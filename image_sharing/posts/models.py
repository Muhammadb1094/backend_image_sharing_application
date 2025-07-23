import uuid

from django.db import models
from django.contrib.auth.models import User

class Image(models.Model):
    """
    Model to store images associated with posts.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to='images/')
    post = models.ForeignKey('ImagePost', on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return f"Image {self.id} for post {self.post.id}"

class ImagePost(models.Model):
    # Use UUID for better distribution
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    caption = models.CharField(max_length=100)

    # Denormalized counters for performance
    likes_count = models.PositiveIntegerField(default=0, db_index=True)

    # Additional fields for a complete social media app
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['created_at']),
            models.Index(fields=['likes_count']),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} - {self.caption[:10]}"


class Like(models.Model):
    # Use UUID for better distribution
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(ImagePost, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        unique_together = ('user', 'post')
        indexes = [
            models.Index(fields=['post', 'created_at']),
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.user.email} likes post {self.post.id}"
