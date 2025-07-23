from posts.models import ImagePost
from rest_framework import serializers


class DefaultPostSerializer(serializers.ModelSerializer):
    """
    Serializer for ImagePost model.
    """
    class Meta:
        model = ImagePost
        fields = "__all__"
        read_only_fields = ['id', 'created_at', 'updated_at', 'likes_count', 'user']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
