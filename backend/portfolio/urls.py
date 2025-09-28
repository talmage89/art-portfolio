from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.http import JsonResponse
from django.urls import reverse
from rest_framework.routers import DefaultRouter

from artwork.views import (
    ArtworkViewSet,
    ImageViewSet,
)
from payments.views import CreateCheckoutSessionView, stripe_webhook, health_check

urlpatterns = static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

router = DefaultRouter()
router.register(r"artworks", ArtworkViewSet)
router.register(r"images", ImageViewSet)

urlpatterns += [
    path("api/", include(router.urls)),
    path("api/auth/", include("rest_framework.urls"), name="api-auth"),
    path(
        "api/create-checkout-session/",
        CreateCheckoutSessionView.as_view(),
        name="create-checkout-session",
    ),
    path("api/stripe-webhook/", stripe_webhook, name="stripe-webhook"),
    path("api/health/", health_check, name="health-check"),
    path("", admin.site.urls),
]
