from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponseBadRequest, HttpResponseNotFound ,JsonResponse, HttpResponse, HttpRequest, HttpResponseRedirect
from django.views import generic
from feed_app.models import Post
from django.shortcuts import redirect
from followers_app.models import Followers 
from profiles_app.forms import UpdateProfileForm, UpdateUserForm
from profiles_app.models import Profile
from allauth.account.views import PasswordChangeView
from django.contrib import messages


# creating a view for changing password - cusotmizing
class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    """
    Overriding Allauth view so we can redirect to a custom page.
    """
    def get_success_url(self) -> str:
        """
        Return the URL to redirect to after processing a valid form.

        Using this instead of just defining the success_url attribute
        because our url has a dynamic element.
        """
        success_url = reverse('profiles_app:custom_change_password')
        return success_url
        

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
        context["total_followers"] = Followers.objects.filter(following=user).count() 
        # follower.followed_by.all().count() if follower defined or 
        # follower.following.all().count()
        if self.request.user.is_authenticated:
            # checking if logged user is following the user that we curently are viewing
            # user is defined as get_object which is retrived from the url slug (username)
            # and self.request.user is the currently logged user
            context['you_follow'] = Followers.objects.filter(following=user, followed_by = self.request.user).exists()
        return context
        
# Creating Follow view 
# This will be a base view
class FollowView(LoginRequiredMixin, generic.base.View):
    http_method_names: list[str] = ["post"]


    def post(self, request, *args, **kwargs):        
        
        # follow_action=request.POST.get('follow_action'),
        # follow_action=request.POST.['follow_action'],
        # user_to_follow=request.POST.get('username_to_follow'),
        # user_to_follow=request.POST.['username_to_follow'],
    
        
        # https://docs.djangoproject.com/en/4.1/ref/request-response/#django.http.QueryDict
        data = request.POST.dict()
        
        # if the required data not in the POST request
        # so if someone will acces this url but will not provide the 
        # required data it will generate a 400 statu code http response - which is bad request
        if 'follow_action' not in data or 'username_to_follow' not in data:
            return HttpResponseBadRequest("Missing data.") # generates 400 - bad request
        
        # try to get the user
        try:
            other_user = User.objects.get(username=data['username_to_follow'])
        except User.DoesNotExist:
            return HttpResponseNotFound("Missing user.") # generates 404 - requested page is not available

        
        # if the intention is to follow
        if data['follow_action'] == 'follow':
            # follow the user
            # https://docs.djangoproject.com/en/4.1/ref/models/querysets/#get-or-create
            follower, created = Followers.objects.get_or_create(
                followed_by = request.user,
                following = other_user,
            )
        else:
            # unfollow the user
            try:
                follower = Followers.objects.get(
                    followed_by = request.user,
                    following = other_user,
                )
            except Followers.DoesNotExist:
                follower = None
        
            # deleteing the folower object
            if follower:
                follower.delete()



        # https://docs.djangoproject.com/en/4.1/ref/request-response/
        return JsonResponse({
            'success': True,
            'wording': "Unfollow" if data['follow_action'] == 'follow' else 'Follow',
            'followers': Followers.objects.filter(following=other_user).count() , 
        })


# creating the ProfileUpdate view
class EditProfileView(LoginRequiredMixin, generic.UpdateView ):
    model = User
    template_name: str = "profiles_app/edit_profile.html"
    slug_field: str = "username" # this exists in User model
    slug_url_kwarg: str = "username" # this is the name of the slug from the url.py -> '<str:username>'
    form_class = UpdateUserForm
    second_form_class = UpdateProfileForm 
    success_url = '/'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        if 'user_form' not in context:
            context['user_form'] = self.form_class(self.request.GET, instance = self.request.user)
        if 'user_form' not in context:
            # context['profile_form'] = self.second_form_class(self.request.GET, self.request.FILES, instance = self.request.user.profile)
            context['profile_form'] = self.second_form_class(self.request.GET, instance = self.request.user.profile)
        return context

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        # return super().get(request, *args, **kwargs)
        super().get(request, *args, **kwargs)
        user_form = self.form_class(instance = request.user)
        # profile_form = self.second_form_class(self.request.FILES ,instance = request.user.profile)
        profile_form = self.second_form_class(instance = request.user.profile)
        return self.render_to_response(
            self.get_context_data(
                object = self.object,
                user_form = user_form,
                profile_form = profile_form,
        ))
    
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        # return super().post(request, *args, **kwargs)
        self.object = self.get_object()
        user_form = self.form_class(request.POST, instance = request.user)
        profile_form = self.second_form_class(request.POST, self.request.FILES,  instance = request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            # check user name - this works alredy
            # check email not in the database
            userdata = user_form.save()
            userdata.save()
            # userdata.save_m2m() # only if amany to many relationship pexists and commit=False was used before
            profiledata = profile_form.save()
            profiledata.save()
            # profiledata.save_m2m() # only if amany to many relationship pexists and commit=False was used before
            # data can be changed before updating / saving to data base
            # userdata = user_form.save(commit=False)
            # check password ?
            # userdata.save()
            # profiledata = profile_form.save(commit=False)
            # profiledata.user = userdata
            # profiledata.save()

            # adding a message indicating a successful update of profile
            messages.add_message(request, messages.SUCCESS, 'Your profile was updated successfully.')

            return redirect('profiles_app:edit_profile', username = userdata.username )
            # return HttpResponseRedirect(self.get_success_url())
        else: 
            return self.render_to_response(
                self.get_context_data(
                    user_form = user_form,
                    profile_form = profile_form,)
            )