from django.contrib.auth.models import User
from users.models import Profile
from rest_framework import serializers



class DefaultProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['followers_count', 'following_count', 'posts_count']
        read_only_fields = ['followers_count', 'following_count', 'posts_count']

class DefaultUserSerializer(serializers.ModelSerializer):
    profile = DefaultProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'email', 'is_active', 'date_joined', 'profile']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['profile'] = DefaultProfileSerializer(instance.profile).data
        return representation
