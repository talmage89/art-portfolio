"""
URL configuration for portfolio project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.routers import DefaultRouter
from artwork.views import (
    ArtworkViewSet,
    ImageViewSet,
    TestEmailSendView,
    PreviewEmailTemplateView,
)
from payments.views import CreateCheckoutSessionView, stripe_webhook

router = DefaultRouter()
router.register(r"artworks", ArtworkViewSet)
router.register(r"images", ImageViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/auth/", include("rest_framework.urls"), name="api-auth"),
    path(
        "api/create-checkout-session/",
        CreateCheckoutSessionView.as_view(),
        name="create-checkout-session",
    ),
    path("api/stripe-webhook/", stripe_webhook, name="stripe-webhook"),
    path(
        "api/test-send-email/",
        TestEmailSendView.as_view(),
        name="test-send-email",
    ),
    path(
        "api/preview-email/",
        PreviewEmailTemplateView.as_view(),
        name="preview-email",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
