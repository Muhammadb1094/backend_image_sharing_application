"""
URL configuration for image post app handles the posts.
"""
from django.urls import path
from . import views


urlpatterns = [
    path('upload-image/', views.UploadImagePost.as_view(), name='upload_image_post'),
    path('feed/', views.FeedImagePostView.as_view(), name='feed'),
    path('all-posts/', views.AllImagePostView.as_view(), name='all_posts'),
    path('like-unlike/<post_id>/', views.LikePostView.as_view(), name='like_post'),
]
