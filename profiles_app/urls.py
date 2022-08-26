from django.urls import path
from profiles_app.views import ProfileDetailView


app_name = 'profiles_app'

urlpatterns = [
    # ex: /profile/
    # example: /profile/bobtester
    path('<str:username>', ProfileDetailView.as_view(), name="detail" ),
]
