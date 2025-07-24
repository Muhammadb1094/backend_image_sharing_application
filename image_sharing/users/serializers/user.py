"""Default serializers for User and Profile models in the image sharing application.
These serializers are used to provide a basic representation of user data,
including profile information such as followers, following, and posts count."""
from django.contrib.auth.models import User
from users.models import Profile
from rest_framework import serializers



class DefaultProfileSerializer(serializers.ModelSerializer):
    """Serializer for the Profile model to include basic user statistics."""
    class Meta:
        """Meta class for DefaultProfileSerializer to define fields and model."""
        model = Profile
        fields = ['followers_count', 'following_count', 'posts_count']
        read_only_fields = ['followers_count', 'following_count', 'posts_count']


class DefaultUserSerializer(serializers.ModelSerializer):
    """Serializer for the User model to include basic user information and profile statistics."""
    profile = DefaultProfileSerializer()
    class Meta:
        """Meta class for DefaultUserSerializer to define fields and model."""
        model = User
        fields = ['id', 'email', 'is_active', 'date_joined', 'profile']

    def to_representation(self, instance: User) -> dict:
        """Customize the representation of the User instance to include profile data."""
        representation = super().to_representation(instance)
        representation['profile'] = DefaultProfileSerializer(instance.profile).data
        return representation
