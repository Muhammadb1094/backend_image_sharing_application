from posts.models import ImagePost, Image
from users.serializers.user import DefaultUserSerializer
from rest_framework import serializers

class ImageSerializer(serializers.ModelSerializer):
    """
    Serializer for individual image in an image post.
    """
    class Meta:
        model = Image
        fields = ['id', 'image', 'post']

class DefaultPostSerializer(serializers.ModelSerializer):

    user = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ImagePost
        fields = "__all__"
        read_only_fields = ['id', 'created_at', 'updated_at', 'likes_count', 'user']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        post = super().create(validated_data)

        for image_file in self.context['request'].FILES.getlist('images'):
            image_serializer = ImageSerializer(data={'image': image_file, 'post': post.id})
            image_serializer.is_valid(raise_exception=True)
            image_serializer.save(post=post)
        return post

    def get_user(self, obj):
        return DefaultUserSerializer(obj.user).data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['images'] = instance.images.all().values_list('image', flat=True)
        return representation
