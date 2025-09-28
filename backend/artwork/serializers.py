from rest_framework import serializers

from .models import Artwork, Image


class ImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        if obj.image:
            return obj.image.url
        return None

    class Meta:
        model = Image
        fields = ["id", "image", "is_main_image", "uploaded_at"]


class ArtworkSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    image_dimensions = serializers.SerializerMethodField()

    def get_images(self, obj):
        images = obj.images.all()
        return ImageSerializer(images, many=True, context=self.context).data

    def get_image_dimensions(self, obj):
        return obj.get_image_dimensions()

    class Meta:
        model = Artwork
        fields = [
            "id",
            "title",
            "painting_number",
            "painting_year",
            "width_inches",
            "height_inches",
            "medium",
            "category",
            "status",
            "price_cents",
            "created_at",
            "image_dimensions",
            "images",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if self.context.get("view").action == "list":
            images = data.pop("images")
            data["images"] = [images[0]] if images else []
        return data
