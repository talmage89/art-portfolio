import uuid
import logging
from django.db import models
from django.core.exceptions import ValidationError
from PIL import Image as PILImage
import os

from orders.models import Order, Shipment

logger = logging.getLogger(__name__)


class Artwork(models.Model):
    STATUS_CHOICES = [
        ("sold", "Sold"),
        ("available", "Available"),
        ("coming_soon", "Coming Soon"),
        ("not_for_sale", "Not for Sale"),
        ("unavailable", "Unavailable"),
    ]

    MEDIUM_CHOICES = [
        ("oil_panel", "Oil on Panel"),
        ("acrylic_panel", "Acrylic on Panel"),
        ("oil_mdf", "Oil on MDF"),
        ("oil_paper", "Oil on Oil Paper"),
        ("unknown", "Unknown"),
    ]

    CATEGORY_CHOICES = [
        ("figure", "Figure"),
        ("landscape", "Landscape"),
        ("multi_figure", "Multi-Figure"),
        ("other", "Other"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    painting_number = models.IntegerField(null=True, blank=True)
    painting_year = models.IntegerField(null=True, blank=True)
    width_inches = models.DecimalField(max_digits=6, decimal_places=4)
    height_inches = models.DecimalField(max_digits=6, decimal_places=4)
    price_cents = models.IntegerField()
    paper = models.BooleanField(default=False)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    medium = models.CharField(max_length=20, choices=MEDIUM_CHOICES)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

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

    sort_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    sold_at = models.DateTimeField(null=True, blank=True)

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
        if (
            hasattr(self, "_prefetched_objects_cache")
            and "images" in self._prefetched_objects_cache
        ):
            images = self._prefetched_objects_cache["images"]
            for image in images:
                if image.is_main_image:
                    return (image.image_width, image.image_height)
            if images:
                return (images[0].image_width, images[0].image_height)
            return None
        else:
            main_images = self.images.filter(is_main_image=True)
            if main_images.exists():
                return (
                    main_images.first().image_width,
                    main_images.first().image_height,
                )
            elif self.images.exists():
                return (
                    self.images.first().image_width,
                    self.images.first().image_height,
                )
            return None


def artwork_image_upload_path(instance, filename):
    ext = filename.split(".")[-1]
    upload_path = f"{instance.artwork.id}_{uuid.uuid4().hex[:8]}.{ext}"
    logger.info(
        f"Upload path generated: {upload_path} for artwork {instance.artwork.id} (filename: {filename})"
    )
    return upload_path


class Image(models.Model):
    artwork = models.ForeignKey(
        Artwork, related_name="images", on_delete=models.CASCADE
    )

    image = models.ImageField(upload_to=artwork_image_upload_path)
    image_width = models.IntegerField(null=True, blank=True, editable=False)
    image_height = models.IntegerField(null=True, blank=True, editable=False)
    is_main_image = models.BooleanField(default=False)

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.image:
            logger.info(
                f"Saving image for artwork {self.artwork.id}: {self.image.name}"
            )
            try:
                with PILImage.open(self.image) as img:
                    self.image_width, self.image_height = img.size
                    logger.info(
                        f"Image dimensions: {self.image_width}x{self.image_height}"
                    )
            except Exception as e:
                logger.error(f"Error reading image dimensions: {e}")

            try:
                super().save(*args, **kwargs)
                logger.info(f"Image saved successfully. Final URL: {self.image.url}")
            except Exception as e:
                logger.error(f"Error saving image: {e}")
                raise
        else:
            logger.warning("Attempting to save Image instance without image file")
            super().save(*args, **kwargs)

    def __str__(self):
        return f"Image for {self.artwork.title}"
