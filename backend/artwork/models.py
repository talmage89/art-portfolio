from django.db import models


class Artwork(models.Model):
    title = models.CharField(max_length=200)
    size = models.CharField(max_length=200)
    price_cents = models.IntegerField()
    status = models.CharField(
        max_length=20, choices=[("available", "Available"), ("sold", "Sold")]
    )
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Image(models.Model):
    artwork = models.ForeignKey(
        Artwork, related_name="images", on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="artwork/")
    is_main_image = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.artwork.title}"
