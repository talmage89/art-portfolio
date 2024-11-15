from rest_framework import serializers

from artwork.serializers import ArtworkSerializer
from .models import Order, Payment, Shipment


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