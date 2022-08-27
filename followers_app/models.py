from django.db import models
from django.db.models import F, Q, Exists
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

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


    def clean(self) -> None:
        # dont allow to follow yourself - databse level
        if self.followed_by.id == self.following.id:
            raise ValidationError(_("You can't follow yourself !!"))

  
    class Meta:
        # https://docs.djangoproject.com/en/4.1/ref/models/options/#unique-together
        # might be deprecated
        # unique_together = ('followed_by','following',)
        constraints = [
            models.UniqueConstraint(fields=['followed_by','following'], name='unique_following_index'), 
            # this will cause an Integrity error this is why we have additionaly def clean defined !
            models.CheckConstraint(check=~Q(followed_by_id = F("following_id")),name='id_cant_be_the_same'),           
        ]

  
    
        