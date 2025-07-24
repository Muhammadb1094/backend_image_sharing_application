"""
This module contains views for user authentication, including signup and login functionalities.
It uses Django REST Framework for API views and serializers for data validation.
"""
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from users.serializers.user import DefaultUserSerializer

from .serializers.auth import SignupSerializer, LoginSerializer


class SignupView(APIView):
    """
    View for user signup, allowing new users to register.
    It validates the input data and creates a new user if valid.
    Returns a token for the newly created user.
    """

    def post(self, request):
        """
        Handles POST requests for user signup.
        Validates the input data using SignupSerializer.
        If valid, creates a new user and returns a token.
        """
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                {
                    "user": DefaultUserSerializer(user).data,
                    "token": token.key},
                status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """View for user login, allowing existing users to authenticate.
    It checks the provided credentials and returns a token if valid."""
    def post(self, request):
        """
        Handles POST requests for user login.
        Validates the input data using LoginSerializer.
        If valid, authenticates the user and returns a token.
        """
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response(
                    {"detail": "Invalid email or password"},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            user = authenticate(username=user.username, password=password)
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                return Response(
                    {
                        "user": DefaultUserSerializer(user).data,
                        "token": token.key},
                    status=status.HTTP_200_OK)
            return Response(
                {"detail": "Invalid email or password"},
                status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
