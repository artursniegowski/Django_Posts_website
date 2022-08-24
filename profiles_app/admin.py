from django.contrib import admin
from profiles_app.models import Profile


# Register Profile model on the admin site
class ProfileAdmin(admin.ModelAdmin):
    pass

admin.site.register(Profile, ProfileAdmin)