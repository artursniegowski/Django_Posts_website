from http.client import HTTPResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import generic
from feed_app.models import Post 
from followers_app.models import Followers
from typing import Any


# Home page view
class HomePageView(generic.TemplateView):
    http_method_names: list[str] = ["get"]
    template_name: str = "feed_app/index.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            # if user logged in we will show a cusotmized list of posts
            # first the post from people we follow and then the rest

            # list of user that we follow - all the user that the logged user is following
            # https://docs.djangoproject.com/en/4.1/ref/models/querysets/#values-list
            following = list(
                Followers.objects.filter(followed_by=self.request.user).values_list('following', flat=True)
            )
            # if list of following is empty
            if not following:
                # show the default posts
                posts = Post.objects.all().order_by("-id")[:60]
            else:
                # show only the post of people we are following
                posts = Post.objects.filter(author__in=following).order_by("-id")[:60] | Post.objects.exclude(author__in=following).order_by("-id")[:60]
        else:
            # else display last 30 post in descending order by id (newest first)
            posts = Post.objects.all().order_by("-id")[:30]
        
        context['posts'] = posts
        return context


# create a detail post view
class PostDetailView(generic.DetailView):
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

    # def dispatch(self, request, *args, **kwargs):
    #     self.request = request
    #     return super().dispatch(request, *args, **kwargs)


    def form_valid(self, form) -> HTTPResponse:
        obj_form = form.save(commit=False)
        obj_form.author = self.request.user
        obj_form.save()
        return super().form_valid(form)


    def post(self, request, *args, **kwargs):        
        
        post = Post.objects.create(
            # request.POST['text']
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