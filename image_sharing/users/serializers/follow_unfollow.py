# serializers.py
from rest_framework import serializers
from users.models import Follow

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['id', 'follower', 'followed', 'created_at']
        read_only_fields = ['id', 'created_at', 'follower']

    def validate(self, data):
        if self.context['request'].user == data['followed']:
            raise serializers.ValidationError("You cannot follow yourself.")
        return data
