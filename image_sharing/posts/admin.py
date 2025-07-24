"""Admin configuration for the image sharing app.
This file registers the models with the Django admin site."""
from django.contrib import admin

from .models import ImagePost, Image, Like
# Register your models here.

class ImagePostAdmin(admin.ModelAdmin):
    """Admin interface for ImagePost model."""
    list_display = ('caption', 'likes_count', 'user')
    search_fields = ('caption',)
    ordering = ('-created_at',)

admin.site.register(ImagePost, ImagePostAdmin)
admin.site.register(Image)
admin.site.register(Like)
