from django.urls import path
from feed_app.views import CreateNewPostView ,HomePageView, PostDetailView


app_name = 'feed_app'

urlpatterns = [
    # ex: /
    path('', HomePageView.as_view(), name="index" ),
    # 1/
    path('<int:pk>/', PostDetailView.as_view(), name="detail" ),
    # new_post/
    path('new_post/', CreateNewPostView.as_view(), name="new_post" ),
]
