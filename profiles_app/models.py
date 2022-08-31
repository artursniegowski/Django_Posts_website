from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from sorl.thumbnail import ImageField

# model for a profile
class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE, # if we delete the user we also delete the profile
        related_name='profile',
    )# User object
    image = ImageField(upload_to='img_profiles')


    def __str__(self) -> str:
        return self.user.username
        

# monitortin a signal for created user
# https://docs.djangoproject.com/en/4.1/topics/signals/#receiver-functions
@receiver(post_save, sender=User)
def create_user_profile(sender, **kwargs):
    """
    Create a new Profile object when a Django User is created.
    """
    if kwargs["created"]:
        Profile.objects.create(user=kwargs["instance"])
