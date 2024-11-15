from django.contrib import admin

from .models import Artwork, Image


class ImageInline(admin.TabularInline):
    model = Image
    extra = 1


class ArtworkAdmin(admin.ModelAdmin):
    inlines = [ImageInline]
    list_display = ["__str__", "sort_order", "size", "price_cents", "status"]
    list_filter = ["status", "created_at"]
    search_fields = ["title"]
    fields = ["title", "sort_order", "size", "price_cents", "status", "shipment"]


class ImageAdmin(admin.ModelAdmin):
    list_display = ["__str__", "artwork", "is_main_image", "uploaded_at"]


admin.site.register(Artwork, ArtworkAdmin)
admin.site.register(Image, ImageAdmin)
