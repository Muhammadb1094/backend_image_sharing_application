# views.py
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.pagination import PageNumberPagination
from .models import Follow
from .serializers.follow_unfollow import FollowSerializer
from .serializers.user import DefaultUserSerializer


class FollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk: int):
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
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk: int):
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
        # Get users that the current user follows
        users = User.objects.exclude(is_staff=True, is_superuser=True).exclude(pk=request.user.pk)

        # Apply pagination
        paginator = PageNumberPagination()
        paginator.page_size = 20
        paginated_users = paginator.paginate_queryset(users, request)

        serializer = DefaultUserSerializer(paginated_users, many=True)
        return paginator.get_paginated_response(serializer.data)
