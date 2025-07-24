"""Models for user profiles and follow relationships in an image sharing application.
This module includes denormalized fields for performance optimization,
and uses UUIDs for follow relationships.
It also includes signals to automatically create profiles and update follow counts."""
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import F, Case, When, Value, IntegerField



class Profile(models.Model):
    """User profile model with denormalized fields for performance optimization."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # Denormalized fields for performance
    followers_count = models.PositiveIntegerField(default=0, db_index=True)
    following_count = models.PositiveIntegerField(default=0, db_index=True)
    posts_count = models.PositiveIntegerField(default=0, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Indexes for denormalized fields to speed up queries"""
        indexes = [
            models.Index(fields=['followers_count']),
            models.Index(fields=['following_count']),
            models.Index(fields=['posts_count']),
        ]

    def __str__(self):
        return self.user.email

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Automatically create a profile when a User is created."""
    if created:
        Profile.objects.create(user=instance)

class Follow(models.Model):
    """Model representing a follow relationship between users.
    This model uses UUIDs for the primary key to ensure better distribution"""
    # Use UUID for better distribution in sharded databases
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        """Unique constraint to prevent duplicate follow relationships"""
        unique_together = ('follower', 'followed')
        indexes = [
            models.Index(fields=['follower', 'created_at']),
            models.Index(fields=['followed', 'created_at']),
            models.Index(fields=['created_at']),
        ]

    def clean(self):
        """Prevent self-following"""
        if self.follower == self.followed:
            raise ValidationError("You cannot follow yourself.")

    def __str__(self):
        return f"{self.follower.username} follows {self.followed.username}"

@receiver(post_save, sender=Follow)
def update_follow_counts_on_create(sender, instance, created, **kwargs):
    """Update follow counts when a Follow relationship is created."""
    if created:
        Profile.objects.filter(user=instance.follower).update(
            following_count=F('following_count') + 1
        )

        Profile.objects.filter(user=instance.followed).update(
            followers_count=F('followers_count') + 1
        )

@receiver(post_delete, sender=Follow)
def update_follow_counts_on_delete(sender, instance, **kwargs):
    """Update follow counts when a Follow relationship is deleted."""
    Profile.objects.filter(user=instance.follower).update(
        following_count=Case(
            When(following_count__gt=0, then=F('following_count') - 1),
            default=Value(0),
            output_field=IntegerField()
        )
    )

    Profile.objects.filter(user=instance.followed).update(
        followers_count=Case(
            When(followers_count__gt=0, then=F('followers_count') - 1),
            default=Value(0),
            output_field=IntegerField()
        )
    )
