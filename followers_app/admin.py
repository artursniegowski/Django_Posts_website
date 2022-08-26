from django.contrib import admin
from followers_app.models import Followers

# Register Followers model on the admin site
class FollowersAdmin(admin.ModelAdmin):
    pass

admin.site.register(Followers, FollowersAdmin)