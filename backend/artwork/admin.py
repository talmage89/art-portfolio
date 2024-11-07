from django.contrib import admin

from .models import Artwork, Image


class ImageInline(admin.TabularInline):
    model = Image
    extra = 1


class ArtworkAdmin(admin.ModelAdmin):
    inlines = [ImageInline]


admin.site.register(Artwork, ArtworkAdmin)
admin.site.register(Image)


# Register your models here.
