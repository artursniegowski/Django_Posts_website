from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from profiles_app.models import Profile

# TODO: add widgets class to the fields
# profile model
class UpdateProfileForm(forms.ModelForm):
    image = forms.FileField(required=False)

    class Meta:
        model = Profile
        fields = ['image']

# TODO: add widgets class to the fields
#  user model
class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(max_length=150, required=True)
    first_name = forms.CharField(max_length=150, required=False)
    last_name = forms.CharField(max_length=150, required=False)
    # password = forms.PasswordInput()
    
    class Meta: 
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    # check if email address already exists 
    # validation of the data and exluding from the current value
    def clean_email(self):
        data = self.cleaned_data['email']
        # the new email cant exists in the data base but not including the current value of the current user
        if User.objects.filter(email=data).exists() and self.instance.email != data: 
            raise ValidationError("This email address already exists.")

        # Always return a value to use as the new cleaned data, even if
        # this method didn't change it.
        return data