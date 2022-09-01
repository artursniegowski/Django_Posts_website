"""mysite_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

# TODO : add a new section after logged in user
# https://dev.to/earthcomfy/django-update-user-profile-33ho
# https://docs.djangoproject.com/en/4.1/topics/auth/default/#django.contrib.auth.views.PasswordResetView
# under home, where the user can update 
# firstname, lastname, username, password, and image (avatar)
# account area wher you can change all of the data 


urlpatterns = [
    path('', include('feed_app.urls', namespace='feed_app')),
    # like /login/ - account_login , /signup/ - account_signup , /logout/ - account_logout , ...
    path('', include('allauth.urls')),
    path('profile/', include('profiles_app.urls', namespace='profiles_app' )),
    # https://django-allauth.readthedocs.io/en/latest/views.html
    path('admin/', admin.site.urls),   
] # + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# During development, you can serve user-uploaded media files from MEDIA_ROOT 
# using the django.views.static.serve() view.
# This is not suitable for production use! For some common deployment 
# strategies, see How to deploy static files.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)