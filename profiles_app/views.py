from django.contrib.auth.models import User
from django.views import generic
from feed_app.models import Post 
# from profiles_app.models import Profile 

# Creating Profile detail view
class ProfileDetailView(generic.DetailView):
    # model = Profile
    # default will be user (from model User -> user)
    # context_object_name: str = "profile"
    model = User 
    http_method_names: list[str] = ['get']
    slug_field: str = "username" # this exists in User model
    slug_url_kwarg: str = "username" # this is the name of the slug from the url.py -> '<str:username>'
    template_name: str = "profiles_app/detail.html"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context["total_posts"] = Post.objects.filter(author=user).count()
        # alternative
        # context["total_posts"] = self.request.user.post_set.all().count()
        # TODO: ADD the total number of posts
        context["total_folowers"] = 'xxxxxx'
        return context
        
    