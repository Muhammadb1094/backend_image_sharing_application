from django.db import models
from django.contrib.auth.models import User
# from django.db.models.signals import post_save, post_delete
# from django.dispatch import receiver
# from django.core.cache import cache
# from django.db.models import F
# import uuid


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # Denormalized fields for performance
    followers_count = models.PositiveIntegerField(default=0, db_index=True)
    following_count = models.PositiveIntegerField(default=0, db_index=True)
    posts_count = models.PositiveIntegerField(default=0, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['followers_count']),
            models.Index(fields=['following_count']),
            models.Index(fields=['posts_count']),
        ]

    def __str__(self):
        return self.user.email


# ""class Follow(models.Model):
#     # Use UUID for better distribution in sharded databases
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
#     followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
#     created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    
#     class Meta:
#         unique_together = ('follower', 'followed')
#         indexes = [
#             models.Index(fields=['follower', 'created_at']),
#             models.Index(fields=['followed', 'created_at']),
#             models.Index(fields=['created_at']),
#         ]
        
#     def clean(self):
#         """Prevent self-following"""
#         if self.follower == self.followed:
#             raise ValidationError("Users cannot follow themselves")
    
#     def __str__(self):
#         return f"{self.follower.username} follows {self.followed.username}"




# # Signal handlers for maintaining denormalized counters
# @receiver(post_save, sender=Follow)
# def update_follow_counts_on_create(sender, instance, created, **kwargs):
#     if created:
#         # Update follower's following count
#         Profile.objects.filter(user=instance.follower).update(
#             following_count=F('following_count') + 1
#         )
        
#         # Update followed user's followers count
#         Profile.objects.filter(user=instance.followed).update(
#             followers_count=F('followers_count') + 1
#         )
        
#         # Clear caches
#         cache.delete(f"user_following_count_{instance.follower.id}")
#         cache.delete(f"user_followers_count_{instance.followed.id}")


# @receiver(post_delete, sender=Follow)
# def update_follow_counts_on_delete(sender, instance, **kwargs):
#     # Update follower's following count
#     Profile.objects.filter(user=instance.follower).update(
#         following_count=F('following_count') - 1
#     )
    
#     # Update followed user's followers count
#     Profile.objects.filter(user=instance.followed).update(
#         followers_count=F('followers_count') - 1
#     )
    
#     # Clear caches
#     cache.delete(f"user_following_count_{instance.follower.id}")
#     cache.delete(f"user_followers_count_{instance.followed.id}")


# @receiver(post_save, sender=Like)
# def update_likes_count_on_create(sender, instance, created, **kwargs):
#     if created:
#         instance.post.increment_likes_count()


# @receiver(post_delete, sender=Like)
# def update_likes_count_on_delete(sender, instance, **kwargs):
#     instance.post.decrement_likes_count()


# @receiver(post_save, sender=ImagePost)
# def update_posts_count_on_create(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.filter(user=instance.user).update(
#             posts_count=F('posts_count') + 1
#         )


# @receiver(post_delete, sender=ImagePost)
# def update_posts_count_on_delete(sender, instance, **kwargs):
#     if not instance.is_deleted:  # Only decrease if it wasn't soft deleted
#         Profile.objects.filter(user=instance.user).update(
#             posts_count=F('posts_count') - 1
#         )


# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)""