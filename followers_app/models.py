from django.db import models
from django.contrib.auth.models import User

# creating a follower model
class Followers(models.Model):
    followed_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE, # so wheneve the followed_by is delete - we delete the raltionship
        # https://docs.djangoproject.com/en/4.1/topics/db/queries/#backwards-related-objects
        # so instead using follower.user_set() , you can write follower.followed_by()
        related_name='followed_by',
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
    )

    def __str__(self) -> str:
        return f"{self.followed_by.id} is following {self.following.id}"

    
    class Meta:
        # https://docs.djangoproject.com/en/4.1/ref/models/options/#unique-together
        # might be deprecated
        # unique_together = ('followed_by','following',)
        constraints = [
            models.UniqueConstraint(fields=['followed_by','following'], name='unique_following_index')
        ]
        