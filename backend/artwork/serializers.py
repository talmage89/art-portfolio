from rest_framework import serializers
from .models import Artwork, Image


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["id", "image", "is_main_image", "uploaded_at"]


class ArtworkSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True)

    class Meta:
        model = Artwork
        fields = [
            "id",
            "title",
            "size",
            "price_cents",
            "status",
            "creation_date",
            "images",
        ]
