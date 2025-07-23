"""
URL configuration for image post app handles the posts.
"""
from django.urls import path
from . import views


urlpatterns = [
    path('upload-image/', views.UploadImagePost.as_view(), name='upload_image_post'),
    # path('login/', views.LoginView.as_view(), name='login'),
]
