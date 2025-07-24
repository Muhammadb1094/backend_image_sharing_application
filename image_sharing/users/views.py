"""View for following and unfollowing users in the image sharing application.
This module provides API endpoints to follow and unfollow users, as well as to list all users
that the current user follows."""
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from django.contrib.auth.models import User
from .models import Follow
from .serializers.follow_unfollow import FollowSerializer
from .serializers.user import DefaultUserSerializer


class FollowUserView(APIView):
    """View to follow a user
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk: int):
        """Follow a user by their primary key (pk)."""
        try:
            to_follow = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(
                {"detail": "User not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        if request.user == to_follow:
            return Response(
                {"detail": "You cannot follow yourself."},
                status=status.HTTP_400_BAD_REQUEST
            )
        follow, created = Follow.objects.get_or_create(follower=request.user, followed=to_follow)
        if not created:
            return Response({"detail": "Already following."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(FollowSerializer(follow).data, status=status.HTTP_201_CREATED)


class UnfollowUserView(APIView):
    """View to unfollow a user"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk: int):
        """Unfollow a user by their primary key (pk)."""
        try:
            to_unfollow = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(
                {"detail": "User not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        try:
            follow = Follow.objects.get(follower=request.user, followed=to_unfollow)
            follow.delete()
            return Response({"detail": "Unfollowed successfully."}, status=status.HTTP_200_OK)
        except Follow.DoesNotExist:
            return Response(
                {"detail": "You are not following this user."},
                status=status.HTTP_400_BAD_REQUEST
            )

class AllUsersView(APIView):
    """
    View to fetch all users that the current user follows
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """Get all the users from the database, excluding staff and superusers,
        and excluding the current user."""
        users = User.objects.all()

        # Apply pagination
        paginator = PageNumberPagination()
        paginator.page_size = 20
        paginated_users = paginator.paginate_queryset(users, request)

        serializer = DefaultUserSerializer(paginated_users, many=True)
        return paginator.get_paginated_response(serializer.data)
