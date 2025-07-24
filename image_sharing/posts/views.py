"""Views for handling image posts in the image sharing application.
This module contains views for uploading image posts, fetching feeds,
and liking posts."""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from .serializers.post import DefaultPostSerializer
from .models import ImagePost, Like



class UploadImagePost(APIView):
    """
    View to handle image post uploads.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Handle POST request to upload an image post.
        """
        serializer = DefaultPostSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FeedImagePostView(APIView):
    """
    View to fetch images from users that the current user follows
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Handle GET request to fetch image posts from followed users.
        Returns a paginated list of posts ordered by creation date."""
        # Get list of users that the current user follows
        following_users = request.user.following.values_list('followed', flat=True)

        # Get posts from followed users, ordered by created_at
        posts = ImagePost.objects.filter(
            user__in=following_users,
            is_deleted=False
        ).order_by('-created_at')

        # Apply pagination
        paginator = PageNumberPagination()
        paginator.page_size = 20
        paginated_posts = paginator.paginate_queryset(posts, request)

        serializer = DefaultPostSerializer(paginated_posts, many=True)
        return paginator.get_paginated_response(serializer.data)

class AllImagePostView(APIView):
    """
    View to fetch all images from users that the current user follows
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Handle GET request to fetch all image posts."""
        # Get posts from all users, ordered by likes_count and created_at
        posts = ImagePost.objects.filter(
            is_deleted=False
        ).order_by('-likes_count', '-created_at')

        # Apply pagination
        paginator = PageNumberPagination()
        paginator.page_size = 20
        paginated_posts = paginator.paginate_queryset(posts, request)

        serializer = DefaultPostSerializer(paginated_posts, many=True)
        return paginator.get_paginated_response(serializer.data)

class LikePostView(APIView):
    """
    View to handle liking a post.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        """
        Handle POST request to like a post.
        """
        try:
            post = ImagePost.objects.get(id=post_id, is_deleted=False)
            if Like.objects.filter(user=request.user, post=post).exists():
                Like.objects.filter(user=request.user, post=post).delete()
                return Response({'message': 'Post unliked successfully'}, status=status.HTTP_200_OK)
            else:
                Like.objects.get_or_create(user=request.user, post=post)
                return Response({'message': 'Post liked successfully'}, status=status.HTTP_200_OK)
        except ImagePost.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as exc:
            return Response(
                {'error': str(exc)},
                status=status.HTTP_400_BAD_REQUEST
            )
