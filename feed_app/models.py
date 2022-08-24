from django.contrib.auth.models import User
from django.db import models

# model for a Post
class Post(models.Model):
    text = models.CharField(max_length=240)
    date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE, # if we delete the user - also delete their posts 
    )

    def __str__(self) -> str:
        return self.text[:100]
