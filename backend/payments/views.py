import stripe
import uuid

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import views
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from artwork.models import Artwork, Order, Payment
from artwork.serializers import OrderSerializer
from utils.order_emails import send_order_confirmation

stripe.api_key = settings.STRIPE_SECRET_KEY
webhook_secret = settings.STRIPE_WEBHOOK_SECRET


class CreateCheckoutSessionView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            product_ids = request.data["product_ids"]
            products = Artwork.objects.filter(id__in=product_ids)

            line_items = []

            for product in products:
                line_items.append(
                    {
                        "price_data": {
                            "currency": "usd",
                            "product_data": {"name": product.title},
                            "unit_amount": product.price_cents,
                        },
                        "quantity": 1,
                    }
                )

            product_ids_str = ",".join(product_ids)

            session = stripe.checkout.Session.create(
                line_items=line_items,
                shipping_address_collection={"allowed_countries": ["US"]},
                shipping_options=[
                    {"shipping_rate": "shr_1QIcy2CQMfNGPu139nrpnjJG"},
                    {"shipping_rate": "shr_1QIcygCQMfNGPu139KfHor3e"},
                ],
                metadata={"product_ids": product_ids_str},
                mode="payment",
                success_url=f"http://localhost:5173/checkout?success=true",
                cancel_url="http://localhost:5173/",
            )
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

        return Response({"url": session.url}, status=status.HTTP_200_OK)


def create_order(session):
    product_ids_str = session["metadata"].get("product_ids", "")
    product_ids = [uuid.UUID(id) for id in product_ids_str.split(",") if id]

    artworks = Artwork.objects.filter(id__in=product_ids)

    order_data = {
        'session_id': session.get("id"),
        'customer_email': session.get("customer_details", {}).get("email"),
        'shipping_rate_id': session.get("shipping_cost", {}).get("shipping_rate"),
        'shipping_name': session.get("shipping_details", {}).get("name"),
        'shipping_address_line1': session.get("shipping_details", {}).get("address", {}).get("line1"),
        'shipping_address_line2': session.get("shipping_details", {}).get("address", {}).get("line2"),
        'shipping_city': session.get("shipping_details", {}).get("address", {}).get("city"),
        'shipping_postal_code': session.get("shipping_details", {}).get("address", {}).get("postal_code"),
        'shipping_state': session.get("shipping_details", {}).get("address", {}).get("state"),
        'shipping_country': session.get("shipping_details", {}).get("address", {}).get("country"),
        'subtotal_cents': session.get("amount_subtotal"),
        'shipping_cents': session.get("total_details", {}).get("amount_shipping"),
        'total_cents': session.get("amount_total"),
        'currency': session.get("currency"),
        "status": session.get("payment_status") == "paid" and "processing" or "pending",
    }

    def apply_artworks_to_order(order, artworks):
        for artwork in artworks:
            artwork.order = order
            artwork.status = "sold"
            artwork.save()

    if Order.objects.filter(session_id=session.id).exists():
        order = Order.objects.get(session_id=session.id)
        serializer = OrderSerializer(instance=order, data=order_data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        apply_artworks_to_order(order, artworks)
    else:
        serializer = OrderSerializer(data=order_data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        apply_artworks_to_order(order, artworks)
        send_order_confirmation(order)

    return order


def fulfill_order(event_type, session):
    session_id = session["id"]

    if event_type == "checkout.session.completed":
        order = create_order(session)

        payment_data = {
            'stripe_payment_intent_id': session.get("payment_intent"),
            'subtotal_cents': session.get("amount_subtotal"),
            'shipping_cents': session.get("total_details", {}).get("amount_shipping"),
            'shipping_stripe_id': session.get("shipping_cost", {}).get("shipping_rate"),
            'total_cents': session.get("amount_total"),
            'currency': session.get("currency"),
        }

        if session.get("payment_status") == "paid":
            order = Order.objects.get(session_id=session_id)
            payment_data['order'] = order
            payment_data['status'] = "succeeded"
            Payment.objects.create(**payment_data)

    elif event_type == "checkout.session.async_payment_succeeded":
        order = Order.objects.get(session_id=session_id)
        order.status = "processing"
        order.save()

        payment_data['order'] = order
        payment_data['status'] = "succeeded"
        Payment.objects.create(**payment_data)

    elif event_type == "checkout.session.async_payment_failed":
        order = Order.objects.get(session_id=session_id)
        order.status = "failed"
        order.save()

        payment_data['order'] = order
        payment_data['status'] = "failed"
        Payment.objects.create(**payment_data)

    elif event_type == "checkout.session.expired":
        try:
            order = Order.objects.get(session_id=session_id)
            order.status = "failed"
            order.save()
        except Order.DoesNotExist:
            pass


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
    except ValueError as e:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    except stripe.error.SignatureVerificationError as e:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    event_type = event["type"]
    session = event["data"]["object"]
    fulfill_order(event_type, session)

    return HttpResponse(status=200)
