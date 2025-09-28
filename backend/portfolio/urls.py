from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.http import JsonResponse
from rest_framework.routers import DefaultRouter

from artwork.views import (
    ArtworkViewSet,
    ImageViewSet,
    TestEmailSendView,
    PreviewEmailTemplateView,
)
from payments.views import CreateCheckoutSessionView, stripe_webhook, health_check


router = DefaultRouter()
router.register(r"artworks", ArtworkViewSet)
router.register(r"images", ImageViewSet)

urlpatterns = [
    path("", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/auth/", include("rest_framework.urls"), name="api-auth"),
    path(
        "api/create-checkout-session/",
        CreateCheckoutSessionView.as_view(),
        name="create-checkout-session",
    ),
    path("api/stripe-webhook/", stripe_webhook, name="stripe-webhook"),
    path("api/health/", health_check, name="health-check"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns.extend(
        [
            path(
                "api/preview-email/",
                PreviewEmailTemplateView.as_view(),
                name="preview-email",
            ),
            path(
                "api/test-send-email/",
                TestEmailSendView.as_view(),
                name="test-send-email",
            ),
        ]
    )
