import django_filters
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser

from utils.order_emails import (
    send_order_confirmation,
    send_shipment_started,
    send_shipment_completed,
)
from orders.models import Order
from .models import Artwork, Image, Order
from .permissions import IsAdminOrReadOnly
from .serializers import (
    ArtworkSerializer,
    ImageSerializer,
)


class ArtworkFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=Artwork.STATUS_CHOICES)

    class Meta:
        model = Artwork
        fields = ["status"]


class ArtworkViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Artwork.objects.all()
    serializer_class = ArtworkSerializer
    parser_classes = (MultiPartParser, FormParser)
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = ArtworkFilter

    def perform_create(self, serializer):
        artwork = serializer.save()
        if "image" in self.request.FILES:
            Image.objects.create(artwork=artwork, image=self.request.FILES["image"])


class ImageViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    parser_classes = (MultiPartParser, FormParser)


class TestEmailSendView(APIView):
    def get(self, request):
        order = Order.objects.first()
        shipment = order.shipments.first()
        send_shipment_started(order, shipment)
        return Response({"message": "Email sent"})


class PreviewEmailTemplateView(APIView):
    TEMPLATE_TO_VIEW = "emails/order_shipped.html"

    def get(self, request):
        order = Order.objects.first()
        if not order:
            return HttpResponse("No orders found to preview")

        artworks = order.artworks.all()
        shipment = order.shipments.first()
        image_urls = {}
        for artwork in artworks:
            if artwork.images.exists():
                image_urls[artwork.id] = (
                    f"{settings.BASE_URL}/media/{artwork.images.first().image}"
                )

        context = {
            "order": order,
            "artworks": artworks,
            "image_urls": image_urls,
            "shipment": shipment,
            "debug": settings.DEBUG,
        }

        return render(request, self.TEMPLATE_TO_VIEW, context)
