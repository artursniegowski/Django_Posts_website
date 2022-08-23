from django.urls import path
from feed_app.views import HomePageView


app_name = 'feed_app'

urlpatterns = [
    # ex: /
    path('', HomePageView.as_view(), name="index" ),
]
