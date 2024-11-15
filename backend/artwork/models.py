import uuid
from django.db import models
from django.core.exceptions import ValidationError

from orders.models import Order, Payment, Shipment


class Artwork(models.Model):
    STATUS_CHOICES = [
        ("available", "Available"),
        ("sold", "Sold"),
        ("unavailable", "Unavailable"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sort_order = models.IntegerField(default=0)
    title = models.CharField(max_length=200)
    size = models.CharField(max_length=200)
    price_cents = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    order = models.ForeignKey(
        Order, on_delete=models.SET_NULL, null=True, blank=True, related_name="artworks"
    )
    shipment = models.ForeignKey(
        Shipment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="artworks",
    )

    class Meta:
        ordering = ["sort_order"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.shipment and self.order != self.shipment.order:
            raise ValidationError(
                "Artwork can only be assigned to shipments from the same order"
            )
        super().save(*args, **kwargs)

    def get_image_dimensions(self):
        main_images = self.images.filter(is_main_image=True)
        if main_images.exists():
            return (main_images.first().image.width, main_images.first().image.height)
        elif self.images.exists():
            return (self.images.first().image.width, self.images.first().image.height)
        return None


class Image(models.Model):
    artwork = models.ForeignKey(
        Artwork, related_name="images", on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="artwork/")
    is_main_image = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.artwork.title}"
