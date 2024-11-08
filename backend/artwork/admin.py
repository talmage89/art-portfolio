from django.contrib import admin

from .models import Artwork, Image, Order, Payment


class ImageInline(admin.TabularInline):
    model = Image
    extra = 1


class ArtworkAdmin(admin.ModelAdmin):
    inlines = [ImageInline]


admin.site.register(Artwork, ArtworkAdmin)
admin.site.register(Image)
admin.site.register(Order)
admin.site.register(Payment)

# Register your models here.
