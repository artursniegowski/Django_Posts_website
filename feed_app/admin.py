from django.contrib import admin
from feed_app.models import Post

# Register Post model on the admin site
class PostAdmin(admin.ModelAdmin):
    pass

admin.site.register(Post, PostAdmin)