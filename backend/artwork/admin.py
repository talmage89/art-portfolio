from django.contrib import admin
from django import forms

from .models import Artwork, Image, Order, Payment, Shipment


class ImageInline(admin.TabularInline):
    model = Image
    extra = 1


class ShipmentInlineForm(forms.ModelForm):
    artworks = forms.ModelMultipleChoiceField(
        queryset=Artwork.objects.none(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Artworks in this shipment",
        help_text="Select which artworks will be included in this shipment",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        parent_order = None
        if self.instance and self.instance.order_id:
            parent_order = self.instance.order
        elif hasattr(self, "parent_instance"):
            parent_order = self.parent_instance

        if parent_order:
            self.fields["artworks"].queryset = Artwork.objects.filter(
                order=parent_order
            )

            if self.instance and self.instance.pk:
                self.initial["artworks"] = self.instance.artworks.all()

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()

            selected_artworks = self.cleaned_data["artworks"]
            for artwork in selected_artworks:
                artwork.shipment = instance
                artwork.save()
            instance.artworks.exclude(id__in=[a.id for a in selected_artworks]).update(
                shipment=None
            )

            instance.save()

        return instance

    class Meta:
        model = Shipment
        fields = [
            "shipping_via",
            "expected_delivery_days",
            "expected_delivery_date",
            "tracking_number",
            "tracking_url",
            "status",
            "artworks",
        ]


class ShipmentInline(admin.StackedInline):
    model = Shipment
    form = ShipmentInlineForm
    extra = 0
    verbose_name = "Shipment"
    verbose_name_plural = "Shipments"

    fieldsets = (
        (
            "Status",
            {"fields": ("status",), "classes": ("wide",)},
        ),
        (
            "Shipping Details",
            {
                "fields": (
                    ("shipping_via", "expected_delivery_days"),
                    "expected_delivery_date",
                ),
                "classes": ("wide",),
            },
        ),
        (
            "Tracking",
            {"fields": (("tracking_number", "tracking_url"),), "classes": ("wide",)},
        ),
        ("Items", {"fields": ("artworks",), "classes": ("wide",)}),
    )

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        formset.form.parent_instance = obj
        return formset


    class Media:
        css = {"all": ("admin/css/shipment_inline.css",)}


class ArtworkAdmin(admin.ModelAdmin):
    inlines = [ImageInline]
    list_display = ["__str__", "sort_order", "size", "price_cents", "status"]
    list_filter = ["status", "created_at"]
    search_fields = ["title"]
    fields = ["title", "sort_order", "size", "price_cents", "status", "shipment"]


class ImageAdmin(admin.ModelAdmin):
    list_display = ["__str__", "artwork", "is_main_image", "uploaded_at"]


class OrderAdmin(admin.ModelAdmin):
    inlines = [ShipmentInline]
    list_display = [
        "__str__",
        "customer_email",
        "status",
        "total_cents",
        "shipping_postal_code",
    ]
    list_filter = ["status", "created_at"]
    search_fields = ["customer_email", "shipping_postal_code"]
    fieldsets = (
        ("Customer Information", {"fields": ("customer_email",)}),
        (
            "Shipping Address",
            {
                "fields": (
                    "shipping_name",
                    "shipping_address_line1",
                    "shipping_address_line2",
                    "shipping_city",
                    "shipping_state",
                    "shipping_postal_code",
                    "shipping_country",
                )
            },
        ),
        (
            "Order Details",
            {
                "fields": (
                    "subtotal_cents",
                    "shipping_cents",
                    "total_cents",
                    "currency",
                    "status",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Technical Details",
            {"fields": ("session_id", "shipping_rate_id"), "classes": ("collapse",)},
        ),
    )


class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        "__str__",
        "order",
        "subtotal_cents",
        "shipping_cents",
        "total_cents",
        "status",
    ]
    list_filter = ["status", "created_at"]
    search_fields = ["order__customer_email", "stripe_payment_intent_id"]
    fieldsets = (
        (
            "Payment Details",
            {
                "fields": (
                    "order",
                    "status",
                    "subtotal_cents",
                    "shipping_cents",
                    "total_cents",
                    "currency",
                )
            },
        ),
        (
            "Stripe Information",
            {
                "fields": ("stripe_payment_intent_id", "shipping_stripe_id"),
                "classes": ("collapse",),
            },
        ),
    )


class ShipmentAdmin(admin.ModelAdmin):
    list_display = ["__str__", "order", "shipping_via", "created_at"]
    list_filter = ["created_at", "shipping_via"]
    search_fields = ["order__customer_email", "tracking_number"]
    fields = [
        "shipping_via",
        "expected_delivery_days",
        "expected_delivery_date",
        "tracking_number",
        "tracking_url",
    ]


admin.site.register(Artwork, ArtworkAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Shipment, ShipmentAdmin)
