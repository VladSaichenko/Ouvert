from django.contrib import admin

from apps.image.models.image import Image


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('profile', 'image', 'created', 'caption', 'content_object',)
