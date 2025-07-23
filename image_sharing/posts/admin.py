from django.contrib import admin

from .models import ImagePost, Image, Like
# Register your models here.

admin.site.register(ImagePost)
admin.site.register(Image)
admin.site.register(Like)
