"""Serializer for handling follow/unfollow actions in the image sharing application.
This serializer validates the follow action and ensures that a user cannot follow themselves."""
from rest_framework import serializers
from users.models import Follow

class FollowSerializer(serializers.ModelSerializer):
    """Serializer for creating and validating follow relationships."""
    class Meta:
        """Meta class for FollowSerializer."""
        model = Follow
        fields = ['id', 'follower', 'followed', 'created_at']
        read_only_fields = ['id', 'created_at', 'follower']

    def validate(self, attrs) -> dict:
        """Validate the follow action."""
        if self.context['request'].user == attrs['followed']:
            raise serializers.ValidationError("You cannot follow yourself.")
        return attrs
