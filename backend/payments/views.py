import json
import math
import time
import uuid
import warnings

import stripe
import shippo
from shippo.models import components

from django.conf import settings
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, views
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle

from artwork.models import Artwork
from orders.models import Order, Payment
from orders.serializers import OrderSerializer
from utils.order_emails import send_order_confirmation

stripe.api_key = settings.STRIPE_SECRET_KEY
webhook_secret = settings.STRIPE_WEBHOOK_SECRET

shippo_sdk = shippo.Shippo(api_key_header=settings.SHIPPO_API_KEY)


class StripeAnonThrottle(AnonRateThrottle):
    rate = "10/min"


def get_shipping_rates(shipping_details):
    try:
        customer_address = shippo_sdk.addresses.create(
            components.AddressCreateRequest(
                name=shipping_details["name"],
                street1=shipping_details["street1"],
                street2=shipping_details.get("street2"),
                city=shipping_details["city"],
                state=shipping_details["state"],
                zip=shipping_details["postalCode"],
                email=shipping_details["email"],
                country=shipping_details.get("country", "US"),
            )
        )

        sender_address = shippo_sdk.addresses.create(
            components.AddressCreateRequest(
                name=settings.SHIPPO_SENDER_NAME,
                street1=settings.SHIPPO_SENDER_STREET1,
                city=settings.SHIPPO_SENDER_CITY,
                state=settings.SHIPPO_SENDER_STATE,
                zip=settings.SHIPPO_SENDER_ZIP,
                country=settings.SHIPPO_SENDER_COUNTRY,
            )
        )

        parcel = shippo_sdk.parcels.create(
            components.ParcelCreateRequest(
                length=10,
                width=10,
                height=10,
                distance_unit=components.DistanceUnitEnum.IN,
                weight="2",
                mass_unit=components.WeightUnitEnum.LB,
            )
        )

        shipment = shippo_sdk.shipments.create(
            components.ShipmentCreateRequest(
                address_from=sender_address,
                address_to=customer_address,
                parcels=[parcel],
                async_=False,
            )
        )

        rates = shipment.rates
        filtered_rates = [
            {
                "service_name": f"{rate.provider} - {rate.servicelevel.name}",
                "amount_cents": int(math.ceil(float(rate.amount)) * 100) - 1,
                "delivery_days": rate.estimated_days,
            }
            for rate in rates
            if len(rate.attributes) > 0
        ]

        return sorted(filtered_rates, key=lambda x: x["amount_cents"])

    except Exception as e:
        raise ValueError(f"SHIPPING ERROR: {str(e)}")


@method_decorator(csrf_exempt, name="dispatch")
class CreateCheckoutSessionView(views.APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    throttle_classes = [StripeAnonThrottle]

    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            #
            # validate request data
            product_ids = data.get("product_ids")
            shipping_details = data.get("shipping_details")

            required_shipping_fields = [
                "name",
                "email",
                "street1",
                "city",
                "state",
                "postalCode",
            ]
            missing_fields = [
                field
                for field in required_shipping_fields
                if field not in shipping_details
            ]
            if missing_fields:
                return Response(
                    f"Missing required shipping fields: {', '.join(missing_fields)}",
                    status=status.HTTP_400_BAD_REQUEST,
                )

            with transaction.atomic():
                #
                # check if products are still available
                products = Artwork.objects.select_for_update().filter(
                    id__in=product_ids
                )
                if len(products) != len(product_ids):
                    return Response(
                        "One or more products not found",
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                unavailable = [p for p in products if p.status != "available"]
                if unavailable:
                    return Response(
                        f"Products {', '.join(str(p.id) for p in unavailable)} not available",
                        status=status.HTTP_400_BAD_REQUEST,
                    )

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

                #
                # get shipping rates
                filtered_rates = get_shipping_rates(shipping_details)
                shipping_options = [
                    {
                        "shipping_rate_data": {
                            "type": "fixed_amount",
                            "fixed_amount": {
                                "amount": rate["amount_cents"],
                                "currency": "usd",
                            },
                            "display_name": rate["service_name"],
                            "delivery_estimate": {
                                "minimum": {
                                    "unit": "business_day",
                                    "value": rate["delivery_days"],
                                },
                                "maximum": {
                                    "unit": "business_day",
                                    "value": rate["delivery_days"],
                                },
                            },
                        }
                    }
                    for rate in filtered_rates
                ]
                shipping_details_str = json.dumps(shipping_details)

                #
                # create checkout session
                session = stripe.checkout.Session.create(
                    customer_email=shipping_details["email"],
                    line_items=line_items,
                    shipping_address_collection=None,
                    shipping_options=shipping_options[:5],
                    mode="payment",
                    success_url=f"{settings.FRONTEND_URL}/cart/?success=true",
                    cancel_url=f"{settings.FRONTEND_URL}/cart/",
                    expires_at=int(time.time() + 60 * 30),
                    payment_method_types=["card"],
                    metadata={
                        "product_ids": product_ids_str,
                        "created_at": str(timezone.now()),
                        "shipping_details": shipping_details_str,
                    },
                )

        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

        return Response({"url": session.url}, status=status.HTTP_200_OK)


def create_order(session):
    payment_intent_id = session.get("payment_intent")
    session_id = session.get("id")

    existing_order = Order.objects.filter(
        Q(stripe_session_id=session_id) | Q(stripe_payment_intent_id=payment_intent_id)
    ).first()

    if existing_order:
        return existing_order

    with transaction.atomic():
        product_ids = [
            uuid.UUID(id)
            for id in session["metadata"].get("product_ids", "").split(",")
            if id
        ]

        artworks = Artwork.objects.select_for_update().filter(id__in=product_ids)

        unavailable = [a for a in artworks if a.status != "available"]
        if unavailable:
            raise ValueError(f"Artworks {unavailable} no longer available")

        shipping_details = session.get("shipping_details", {}) or {}
        shipping_address = shipping_details.get("address", {}) or {}
        total_details = session.get("total_details", {}) or {}
        shipping_cost = session.get("shipping_cost", {}) or {}
        customer_details = session.get("customer_details", {}) or {}

        order_data = {
            "stripe_session_id": session.get("id"),
            "stripe_payment_intent_id": payment_intent_id,
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

        serializer = OrderSerializer(data=order_data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()

        Artwork.objects.filter(id__in=product_ids).update(
            order=order, status="sold", sold_at=timezone.now()
        )

        try:
            send_order_confirmation(order)
        except Exception as e:
            warnings.warn(
                f"Failed to send order confirmation email: {str(e)}", RuntimeWarning
            )

    return order


def fulfill_order(event_type, session):
    payment_intent_id = session.get("payment_intent")

    try:
        if event_type == "checkout.session.completed":
            order = create_order(session)

            payment_data = {
                "stripe_payment_intent_id": session.get("payment_intent"),
                "subtotal_cents": session.get("amount_subtotal"),
                "shipping_cents": session.get("total_details", {}).get(
                    "amount_shipping", 0
                ),
                "shipping_stripe_id": session.get("shipping_cost", {}).get(
                    "shipping_rate"
                ),
                "total_cents": session.get("amount_total"),
                "currency": session.get("currency"),
            }

            if session.get("payment_status") == "paid":
                order = Order.objects.get(stripe_payment_intent_id=payment_intent_id)
                payment_data["order"] = order
                payment_data["status"] = "succeeded"
                Payment.objects.create(**payment_data)

        elif event_type in [
            "checkout.session.async_payment_succeeded",
            "checkout.session.async_payment_failed",
        ]:
            with transaction.atomic():
                order = Order.objects.get(stripe_payment_intent_id=payment_intent_id)
                order.status = "processing" if "succeeded" in event_type else "failed"
                order.save()

                payment_data["order"] = order
                payment_data["status"] = (
                    "succeeded" if "succeeded" in event_type else "failed"
                )
                Payment.objects.create(**payment_data)

        elif event_type == "checkout.session.expired":
            try:
                order = Order.objects.get(stripe_payment_intent_id=payment_intent_id)
                order.status = "failed"
                order.save()
            except Order.DoesNotExist:
                pass

    except Exception as e:
        warnings.warn(
            f"Error processing webhook {event_type}: {str(e)}", RuntimeWarning
        )


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
    except ValueError as e:
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

    event_type = event["type"]
    session = event["data"]["object"]
    fulfill_order(event_type, session)

    return HttpResponse(status=200)


def health_check(request):
    return JsonResponse({"status": "ok"})
