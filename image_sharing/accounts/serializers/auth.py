"""Serializers for user authentication in the image sharing application.
This module contains serializers for user signup and login processes.
It ensures that user data is validated and processed correctly."""
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class SignupSerializer(serializers.ModelSerializer):
    """Serializer for user signup."""
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        """Meta class for SignupSerializer."""
        model = User
        fields = ['email', 'password']

    def validate_email(self, value):
        """Validate that the email is unique and in lowercase."""
        if User.objects.filter(email=value.lower()).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['email'].lower(),
            email=validated_data['email'].lower(),
            password=validated_data['password']
        )
        return user


class LoginSerializer(serializers.Serializer):
    """Serializer for user login."""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)

    def validate(self, attrs):
        attrs['email'] = attrs['email'].lower()
        email = attrs.get('email')
        password = attrs.get('password')

        if not email or not password:
            raise serializers.ValidationError("Email and password are required.")
        if '@' not in email:
            raise serializers.ValidationError("Enter a valid email address.")
        return attrs
