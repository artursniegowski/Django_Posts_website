from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# model for a profile
class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE, # if we delete the user we also delete the profile
        related_name='profile',
    )# User object

    def __str__(self) -> str:
        return self.user.username

# monitortin a signal for created user
@receiver(post_save, sender=User)
def create_user_profile(sender, **kwargs):
    """
    Create a new Profile object when a Django User is created.
    """
    if kwargs["created"]:
        Profile.objects.create(user=kwargs["instance"])
