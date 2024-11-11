from django.conf import settings
from django.template.loader import render_to_string
from .mailgun import send_mailgun_email

from artwork.templatetags.artwork_tags import cents_to_dollars, get_item
from django.template.defaultfilters import register

register.filter("cents_to_dollars", cents_to_dollars)
register.filter("get_item", get_item)

USE_TESTING_EMAIL = True


def send_order_email(order, template_name, subject, shipment=None):
    artworks = order.artworks.all()
    image_urls = {}
    for artwork in artworks:
        if artwork.images.exists():
            image_urls[artwork.id] = (
                f"{settings.BASE_URL}/media/{artwork.images.first().image}"
            )

    context = {
        "order": order,
        "artworks": artworks,
        "image_urls": image_urls,
    }

    if shipment is not None:
        context["shipment"] = shipment

    text_content = render_to_string(f"emails/{template_name}.txt", context)
    html_content = render_to_string(f"emails/{template_name}.html", context)

    send_mailgun_email(
        subject=subject,
        message=text_content,
        to_email=(
            settings.TESTING_EMAIL_RECIPIENT
            if USE_TESTING_EMAIL
            else order.customer_email
        ),
        html=html_content,
    )


def send_order_confirmation(order):
    send_order_email(order, "order_confirmation", "Your order has been received!")


def send_shipment_started(order, shipment):
    send_order_email(order, "order_shipped", "Your order has shipped!", shipment)


def send_shipment_completed(order, shipment):
    send_order_email(
        order, "order_delivered", "Your order has been delivered!", shipment
    )
