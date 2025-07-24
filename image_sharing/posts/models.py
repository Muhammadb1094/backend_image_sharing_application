"""Models for image posts and associated likes in an image sharing application.
This module includes denormalized fields for performance optimization,
and uses UUIDs for better distribution in sharded databases.
It also includes signals to automatically update post and like counts."""
import uuid
from users.models import Profile

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import F, Case, When, Value, IntegerField


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

    def increment_likes_count(self):
        self.likes_count = F('likes_count') + 1
        self.save(update_fields=['likes_count'])

    def decrement_likes_count(self):
        self.likes_count = F('likes_count') - 1
        self.save(update_fields=['likes_count'])

    def __str__(self):
        return f"{self.user.email} - {self.caption[:10]}"


@receiver(post_save, sender=ImagePost)
def update_posts_count_on_create(sender, instance, created, **kwargs):
    if created:
        Profile.objects.filter(user=instance.user).update(
            posts_count=F('posts_count') + 1
        )


@receiver(post_delete, sender=ImagePost)
def update_posts_count_on_delete(sender, instance, **kwargs):
    if not instance.is_deleted:  # Only decrease if it wasn't soft deleted
        Profile.objects.filter(user=instance.user).update(
            posts_count=Case(
                When(posts_count__gt=0, then=F('posts_count') - 1),
                default=Value(0),
                output_field=IntegerField()
            )
        )


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

@receiver(post_delete, sender=Like)
def update_likes_count_on_delete(sender, instance, **kwargs):
    instance.post.decrement_likes_count()

@receiver(post_save, sender=Like)
def update_likes_count_on_create(sender, instance, created, **kwargs):
    if created:
        instance.post.increment_likes_count()
