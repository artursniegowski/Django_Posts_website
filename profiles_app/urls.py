from django.urls import path
from profiles_app.views import FollowView, ProfileDetailView


app_name = 'profiles_app'

urlpatterns = [
    # ex: /profile/
    # example: /profile/bobtester
    path('<str:username>', ProfileDetailView.as_view(), name="detail" ),
    # example: /profile/bobtester/follow
    path('<str:username>/follow', FollowView.as_view(), name="follow" ),
]
