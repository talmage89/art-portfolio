import uuid
from django.db import models


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session_id = models.CharField(max_length=200)
    customer_email = models.EmailField()
    shipping_rate_id = models.CharField(max_length=200)
    shipping_name = models.CharField(max_length=200)
    shipping_address_line1 = models.CharField(max_length=200)
    shipping_address_line2 = models.CharField(max_length=200, null=True, blank=True)
    shipping_city = models.CharField(max_length=200)
    shipping_postal_code = models.CharField(max_length=200)
    shipping_state = models.CharField(max_length=200)
    shipping_country = models.CharField(max_length=200)
    total_cents = models.IntegerField()
    currency = models.CharField(max_length=200)
    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("processing", "Processing"),
            ("shipped", "Shipped"),
            ("completed", "Completed"),
            ("failed", "Failed"),
            ("refunded", "Refunded"),
        ],
    )

    def __str__(self):
        return f"Order {self.id} for {self.customer_email} - Stripe Session: {self.session_id}"


class Artwork(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(
        Order, on_delete=models.SET_NULL, null=True, blank=True, related_name="artworks"
    )
    title = models.CharField(max_length=200)
    size = models.CharField(max_length=200)
    price_cents = models.IntegerField()
    status = models.CharField(
        max_length=20, choices=[("available", "Available"), ("sold", "Sold")]
    )
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["order"]


class Image(models.Model):
    artwork = models.ForeignKey(
        Artwork, related_name="images", on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="artwork/")
    is_main_image = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.artwork.title}"


class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    stripe_payment_intent_id = models.CharField(max_length=200)
    subtotal_cents = models.IntegerField()
    shipping_cents = models.IntegerField()
    shipping_stripe_id = models.CharField(max_length=200)
    total_cents = models.IntegerField()
    currency = models.CharField(max_length=200)
    status = models.CharField(
        max_length=20,
        choices=[
            ("succeeded", "Succeeded"),
            ("failed", "Failed"),
            ("refunded", "Refunded"),
        ],
    )

    def __str__(self):
        return f"Payment {self.id} for Order {self.order.id} - Stripe Payment Intent: {self.stripe_payment_intent_id}"
