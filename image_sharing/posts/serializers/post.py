"""Serializer for ImagePost model in the image sharing application.
This serializer handles the creation and representation of image posts,
including associated images and user information."""
from posts.models import ImagePost, Image
from users.serializers.user import DefaultUserSerializer
from rest_framework import serializers

class ImageSerializer(serializers.ModelSerializer):
    """Serializer for individual image in an image post."""
    class Meta:
        """Meta class for ImageSerializer."""
        model = Image
        fields = ['id', 'image', 'post']

class DefaultPostSerializer(serializers.ModelSerializer):
    """Serializer for ImagePost model with user and images included.
    This serializer is used to create and retrieve image posts."""
    user = serializers.SerializerMethodField(read_only=True)

    class Meta:
        """Meta class for DefaultPostSerializer."""
        model = ImagePost
        fields = "__all__"
        read_only_fields = ['id', 'created_at', 'updated_at', 'likes_count', 'user']

    def create(self, validated_data) -> ImagePost:
        """Create a new ImagePost instance with associated images."""
        validated_data['user'] = self.context['request'].user
        post = super().create(validated_data)

        for image_file in self.context['request'].FILES.getlist('images'):
            image_serializer = ImageSerializer(data={'image': image_file, 'post': post.id})
            image_serializer.is_valid(raise_exception=True)
            image_serializer.save(post=post)
        return post

    def get_user(self, obj) -> dict:
        """Get the user information for the post image object."""
        return DefaultUserSerializer(obj.user).data

    def to_representation(self, instance) -> dict:
        """Customize the representation of the ImagePost instance."""
        representation = super().to_representation(instance)
        representation['images'] = instance.images.all().values_list('image', flat=True)
        return representation
