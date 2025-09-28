from django.contrib import admin

from .models import Artwork, Image


class ImageInline(admin.TabularInline):
    model = Image
    extra = 1
    fields = [
        "image",
        "is_main_image",
        "image_width",
        "image_height",
        "uploaded_at",
    ]
    readonly_fields = ["image_width", "image_height", "uploaded_at"]


class ArtworkAdmin(admin.ModelAdmin):
    inlines = [ImageInline]
    list_display = [
        "__str__",
        "painting_number",
        "sort_order",
        "width_inches",
        "height_inches",
        "price_cents",
        "status",
    ]
    list_filter = ["status", "created_at", "medium", "category"]
    search_fields = ["title"]


class ImageAdmin(admin.ModelAdmin):
    list_display = [
        "__str__",
        "artwork",
        "is_main_image",
        "image_width",
        "image_height",
        "uploaded_at",
    ]
    readonly_fields = ["image_width", "image_height", "uploaded_at"]
    fields = [
        "artwork",
        "image",
        "is_main_image",
        "image_width",
        "image_height",
        "uploaded_at",
    ]


admin.site.register(Artwork, ArtworkAdmin)
admin.site.register(Image, ImageAdmin)
