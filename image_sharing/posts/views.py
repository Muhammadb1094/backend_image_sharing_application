from django.shortcuts import render


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers.post import DefaultPostSerializer


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
