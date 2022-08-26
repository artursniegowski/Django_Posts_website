from cgitb import text
from http.client import HTTPResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import generic
from feed_app.models import Post 

# Home page view
class HomePageView(generic.ListView):
    context_object_name: str = "posts"
    http_method_names: list[str] = ["get"]
    model = Post
    template_name: str = "feed_app/index.html"
    queryset = Post.objects.all().order_by("-id")[:30]

# create a detail post view
class PostDetailView(generic.DeleteView):
    # by default if model is Post the context will be post
    # context_object_name: str = "post"
    http_method_names: list[str] = ["get"]
    template_name: str = "feed_app/detail.html"
    model = Post


# Note that if you don’t specify the login_url parameter, you’ll need to ensure 
# that the settings.LOGIN_URL and your login view are properly associated. 
# settings.LOGIN_URL = '/login/' - this is set in the settings
class CreateNewPostView(LoginRequiredMixin, generic.CreateView):
    model = Post
    template_name = "feed_app/create_new_post.html"
    fields = ['text']
    success_url = '/'
    # login_url = '/login/'

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        return super().dispatch(request, *args, **kwargs)


    def form_valid(self, form) -> HTTPResponse:
        obj_form = form.save(commit=False)
        obj_form.author = self.request.user
        obj_form.save()
        return super().form_valid(form)

    
    def post(self, request, *args, **kwargs):        
        
        post = Post.objects.create(
            text=request.POST.get('text'),
            author = request.user,
        )
        
        return render(
            request,
            "feed_app/includes/post.html",
            {
                "post": post,
                "show_detail_link": True, 
            },
            # https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types
            # https://www.techonthenet.com/html/mime_type.php
            content_type='application/html'
        )