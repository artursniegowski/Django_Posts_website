from django.urls import path
from profiles_app.views import CustomPasswordChangeView, EditProfileView, FollowView, ProfileDetailView

app_name = 'profiles_app'

urlpatterns = [
    # ex: /profile/
    # example: /profile/change_password/
    path('change_password/', CustomPasswordChangeView.as_view(), name='custom_change_password'),
    # example: /profile/bobtester
    path('<str:username>/', ProfileDetailView.as_view(), name="detail" ),
    # example: /profile/bobtester/edit_profile
    path('<str:username>/edit_profile/', EditProfileView.as_view() , name="edit_profile" ),
    # example: /profile/bobtester/follow
    path('<str:username>/follow/', FollowView.as_view(), name="follow" ),
]
