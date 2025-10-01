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


class ArtworkListSerializer(serializers.ModelSerializer):
    """
    Optimized serializer for list view - only includes first image.

    Performance optimizations:
    - Only serializes 1 image per artwork (not all images)
    - Accesses prefetched data to avoid N+1 queries
    - Manually builds image dict to avoid ImageSerializer overhead
    """

    images = serializers.SerializerMethodField()
    image_dimensions = serializers.SerializerMethodField()

    def get_images(self, obj):
        """Get first image from prefetched images - avoids serializing unused images"""
        if (
            hasattr(obj, "_prefetched_objects_cache")
            and "images" in obj._prefetched_objects_cache
        ):
            images = obj._prefetched_objects_cache["images"]
            if images:
                first_image = images[0]
                return [
                    {
                        "id": first_image.id,
                        "image": first_image.image.url if first_image.image else None,
                        "is_main_image": first_image.is_main_image,
                        "uploaded_at": first_image.uploaded_at,
                    }
                ]
        return []

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


class ArtworkSerializer(serializers.ModelSerializer):
    """Full serializer for detail view - includes all images"""

    images = serializers.SerializerMethodField()
    image_dimensions = serializers.SerializerMethodField()

    def get_images(self, obj):
        # Access prefetched images if available
        if (
            hasattr(obj, "_prefetched_objects_cache")
            and "images" in obj._prefetched_objects_cache
        ):
            images = obj._prefetched_objects_cache["images"]
        else:
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
