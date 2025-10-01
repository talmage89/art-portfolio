import django_filters
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.db.models import Prefetch
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.exceptions import NotFound
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
    ArtworkListSerializer,
    ImageSerializer,
)


class ArtworkFilter(django_filters.FilterSet):
    status = django_filters.MultipleChoiceFilter(
        choices=Artwork.STATUS_CHOICES,
        lookup_expr="in",
        field_name="status",
        conjoined=False,
    )

    class Meta:
        model = Artwork
        fields = ["status"]

    def filter_queryset(self, queryset):
        # Get status values
        status_values = self.form.cleaned_data.get("status", [])
        if status_values:
            queryset = queryset.filter(status__in=status_values)
        return queryset


class ArtworkViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Artwork.objects.all()
    serializer_class = ArtworkSerializer
    parser_classes = (MultiPartParser, FormParser)
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = ArtworkFilter

    def get_serializer_class(self):
        """Use optimized serializer for list view"""
        if self.action == "list":
            return ArtworkListSerializer
        return ArtworkSerializer

    def perform_create(self, serializer):
        artwork = serializer.save()
        if "image" in self.request.FILES:
            Image.objects.create(artwork=artwork, image=self.request.FILES["image"])

    def get_queryset(self):
        queryset = super().get_queryset()

        if "status" not in self.request.query_params:
            queryset = queryset.filter(
                status__in=["available", "coming_soon", "sold", "not_for_sale"]
            )

        queryset = queryset.prefetch_related(
            Prefetch("images", queryset=Image.objects.order_by("-is_main_image"))
        ).order_by("sort_order")

        return queryset

    def get_object(self):
        try:
            obj = super().get_object()
            if obj.status not in ["available", "coming_soon", "sold", "not_for_sale"]:
                raise NotFound()
            return obj
        except NotFound:
            raise NotFound("Artwork not found")


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
