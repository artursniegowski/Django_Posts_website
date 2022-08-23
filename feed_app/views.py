from django.views import generic

from feed_app.models import Post 

# Home page view
class HomePageView(generic.ListView):
    context_object_name: str = "posts"
    http_method_names: list[str] = ["get"]
    model = Post
    template_name: str = "feed_app/index.html"
    queryset = Post.objects.all().order_by("-id")[:30]