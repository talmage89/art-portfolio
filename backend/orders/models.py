import uuid
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

from utils.order_emails import send_shipment_started, send_shipment_completed


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    stripe_session_id = models.CharField(max_length=200, unique=True, null=True)
    stripe_payment_intent_id = models.CharField(max_length=200, unique=True, null=True)
    customer_email = models.EmailField()
    shipping_rate_id = models.CharField(max_length=200)
    shipping_name = models.CharField(max_length=200)
    shipping_address_line1 = models.CharField(max_length=200)
    shipping_address_line2 = models.CharField(max_length=200, null=True, blank=True)
    shipping_city = models.CharField(max_length=200)
    shipping_postal_code = models.CharField(max_length=200)
    shipping_state = models.CharField(max_length=200)
    shipping_country = models.CharField(max_length=200)
    subtotal_cents = models.IntegerField()
    shipping_cents = models.IntegerField()
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
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order made by {self.customer_email}"


class Payment(models.Model):
    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, related_name="payment"
    )
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
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment made by {self.order.customer_email}"


class Shipment(models.Model):
    STATUS_CHOICES = [
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
    ]

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="shipments")
    shipping_via = models.CharField(max_length=200)
    expected_delivery_days = models.CharField(max_length=200, null=True, blank=True)
    expected_delivery_date = models.DateField(null=True, blank=True)
    tracking_number = models.CharField(max_length=200, null=True, blank=True)
    tracking_url = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="shipped")
    shipment_started_email_sent_at = models.DateTimeField(null=True, blank=True)
    shipment_completed_email_sent_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Shipment #{self.pk}"

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super().save(*args, **kwargs)

        if is_new:
            return

        self.refresh_from_db()

        if self.artworks.all().count() == 0:
            raise ValidationError("Shipment must have at least one artwork")

        # Send emails if they haven't been sent yet
        if self.shipment_started_email_sent_at is None:
            send_shipment_started(self.order, self)
            self.shipment_started_email_sent_at = timezone.now()
            super().save(update_fields=["shipment_started_email_sent_at"])
        if self.status == "delivered" and self.shipment_completed_email_sent_at is None:
            send_shipment_completed(self.order, self)
            self.shipment_completed_email_sent_at = timezone.now()
            super().save(update_fields=["shipment_completed_email_sent_at"])

        # Update order status
        unshipped_order_artworks = self.order.artworks.filter(shipment__isnull=True)
        if self.order.status == "processing" and unshipped_order_artworks.count() == 0:
            self.order.status = "shipped"
            self.order.save()
        elif self.order.shipments.exclude(status="delivered").count() == 0:
            self.order.status = "completed"
            self.order.save()
