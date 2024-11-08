from django.conf import settings
from django.template.loader import render_to_string
from .mailgun import send_mailgun_email


def send_order_confirmation(order):
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

    text_content = render_to_string("emails/order_confirmation.txt", context)
    html_content = render_to_string("emails/order_confirmation.html", context)

    subject = f"Order Confirmation #{order.id}"

    send_mailgun_email(
        subject=subject,
        message=text_content,
        # to_email=order.customer_email,
        to_email=settings.TESTING_EMAIL_RECIPIENT,
        html=html_content,
    )
