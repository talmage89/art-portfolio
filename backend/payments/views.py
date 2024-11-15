import stripe
import uuid
import warnings

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import views
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from artwork.models import Artwork
from orders.models import Order, Payment
from orders.serializers import OrderSerializer
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
                    {"shipping_rate": "shr_1QL6h5KQhljGwEslWFE34xvr"},
                ],
                metadata={"product_ids": product_ids_str},
                mode="payment",
                success_url=f"{settings.FRONTEND_URL}/checkout/success",
                cancel_url=f"{settings.FRONTEND_URL}/",
            )
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

        return Response({"url": session.url}, status=status.HTTP_200_OK)


def create_order(session):
    product_ids_str = session["metadata"].get("product_ids", "")
    product_ids = [uuid.UUID(id) for id in product_ids_str.split(",") if id]

    artworks = Artwork.objects.filter(id__in=product_ids)

    shipping_details = session.get("shipping_details", {}) or {}
    shipping_address = shipping_details.get("address", {}) or {}
    total_details = session.get("total_details", {}) or {}
    shipping_cost = session.get("shipping_cost", {}) or {}
    customer_details = session.get("customer_details", {}) or {}

    order_data = {
        "session_id": session.get("id"),
        "customer_email": customer_details.get("email"),
        "shipping_rate_id": shipping_cost.get("shipping_rate"),
        "shipping_name": shipping_details.get("name"),
        "shipping_address_line1": shipping_address.get("line1"),
        "shipping_address_line2": shipping_address.get("line2"),
        "shipping_city": shipping_address.get("city"),
        "shipping_postal_code": shipping_address.get("postal_code"),
        "shipping_state": shipping_address.get("state"),
        "shipping_country": shipping_address.get("country"),
        "subtotal_cents": session.get("amount_subtotal"),
        "shipping_cents": total_details.get("amount_shipping"),
        "total_cents": session.get("amount_total"),
        "currency": session.get("currency"),
        "status": (
            "processing" if session.get("payment_status") == "paid" else "pending"
        ),
    }

    def apply_artworks_to_order(order, artworks):
        for artwork in artworks:
            artwork.order = order
            artwork.status = "sold"
            artwork.save()

    if Order.objects.filter(session_id=session.id).exists():
        order = Order.objects.get(session_id=session.id)
        serializer = OrderSerializer(instance=order, data=order_data)
    else:
        serializer = OrderSerializer(data=order_data)

    serializer.is_valid(raise_exception=True)
    order = serializer.save()
    
    apply_artworks_to_order(order, artworks)

    try:
        send_order_confirmation(order)
    except Exception as e:
        warnings.warn(
            f"Failed to send order confirmation email: {str(e)}", RuntimeWarning
        )

    return order


def fulfill_order(event_type, session):
    session_id = session["id"]

    if event_type == "checkout.session.completed":
        order = create_order(session)

        payment_data = {
            "stripe_payment_intent_id": session.get("payment_intent"),
            "subtotal_cents": session.get("amount_subtotal"),
            "shipping_cents": session.get("total_details", {}).get(
                "amount_shipping", 0
            ),
            "shipping_stripe_id": session.get("shipping_cost", {}).get("shipping_rate"),
            "total_cents": session.get("amount_total"),
            "currency": session.get("currency"),
        }

        if session.get("payment_status") == "paid":
            order = Order.objects.get(session_id=session_id)
            payment_data["order"] = order
            payment_data["status"] = "succeeded"
            Payment.objects.create(**payment_data)

    elif event_type == "checkout.session.async_payment_succeeded":
        order = Order.objects.get(session_id=session_id)
        order.status = "processing"
        order.save()

        payment_data["order"] = order
        payment_data["status"] = "succeeded"
        Payment.objects.create(**payment_data)

    elif event_type == "checkout.session.async_payment_failed":
        order = Order.objects.get(session_id=session_id)
        order.status = "failed"
        order.save()

        payment_data["order"] = order
        payment_data["status"] = "failed"
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
        print("ValueError", e)
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
    except stripe.error.SignatureVerificationError as e:
        print("SignatureVerificationError", e)
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

    event_type = event["type"]
    session = event["data"]["object"]
    fulfill_order(event_type, session)

    return HttpResponse(status=200)
