from django.db import models

# model for a Post
class Post(models.Model):
    text = models.CharField(max_length=240)
    date = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.text[:100]
