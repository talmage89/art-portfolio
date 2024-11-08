from rest_framework import serializers
from .models import Artwork, Image, Order, Payment, Shipment


class ImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        request = self.context.get("request")
        if request and obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None

    class Meta:
        model = Image
        fields = ["id", "image", "is_main_image", "uploaded_at"]


class ArtworkSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    def get_images(self, obj):
        images = obj.images.all()
        sorted_images = sorted(images, key=lambda x: not x.is_main_image)
        return ImageSerializer(sorted_images, many=True, context=self.context).data

    class Meta:
        model = Artwork
        fields = [
            "id",
            "title",
            "size",
            "price_cents",
            "status",
            "created_at",
            "images",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if self.context.get("view").action == "list":
            images = data.pop("images")
            data["images"] = [images[0]]
        return data


class OrderSerializer(serializers.ModelSerializer):
    artworks = serializers.SerializerMethodField()
    shipments = serializers.SerializerMethodField()
    payment = serializers.SerializerMethodField()

    def get_artworks(self, obj):
        return ArtworkSerializer(
            obj.artworks.all(), many=True, context=self.context
        ).data

    def get_payment(self, obj):
        return PaymentSerializer(obj.payment, context=self.context).data

    def get_shipments(self, obj):
        return ShipmentSerializer(
            obj.shipments.all(), many=True, context=self.context
        ).data

    class Meta:
        model = Order
        fields = "__all__"


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class ShipmentSerializer(serializers.ModelSerializer):
    artworks = serializers.SerializerMethodField()

    def get_artworks(self, obj):
        return ArtworkSerializer(
            obj.artworks.all(), many=True, context=self.context
        ).data

    class Meta:
        model = Shipment
        fields = "__all__"
