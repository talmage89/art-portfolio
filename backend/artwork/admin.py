from django.contrib import admin

from .models import Artwork, Image, Order, Payment


class ImageInline(admin.TabularInline):
    model = Image
    extra = 1


class ArtworkAdmin(admin.ModelAdmin):
    inlines = [ImageInline]
    list_display = ["__str__", "sort_order", "size", "price_cents", "status"]
    list_filter = ["status", "created_at"]


class ImageAdmin(admin.ModelAdmin):
    list_display = ["__str__", "artwork", "is_main_image", "uploaded_at"]


class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "__str__",
        "customer_email",
        "status",
        "total_cents",
        "shipping_postal_code",
    ]
    list_filter = ["status", "created_at"]


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


admin.site.register(Artwork, ArtworkAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment, PaymentAdmin)
