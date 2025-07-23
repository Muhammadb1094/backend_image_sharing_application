"""
URL configuration for accounts app handles the authentication.
"""
from django.urls import path
from . import views


urlpatterns = [
    path('follow/<int:pk>/', views.FollowUserView.as_view(), name='follow'),
    path('unfollow/<int:pk>/', views.UnfollowUserView.as_view(), name='unfollow'),
    path('all-users/', views.AllUsersView.as_view(), name='all_users'),

]
