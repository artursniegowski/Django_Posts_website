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

# Form for updating user data
class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(min_length=2, max_length=150, required=True,
        widget=forms.TextInput(
            attrs={
                'class':'block py-2.5 px-0 w-full text-sm text-gray-900 bg-transparent border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer',
                'placeholder':' ',
            }
        ))
    email = forms.EmailField(min_length=2, max_length=150, required=True,
        widget=forms.EmailInput(
            attrs={
                'class':'block py-2.5 px-0 w-full text-sm text-gray-900 bg-transparent border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer',
                'placeholder':' ',
            }
        ))
    first_name = forms.CharField(max_length=150, required=False,
        widget=forms.TextInput(
            attrs={
                'class':'block py-2.5 px-0 w-full text-sm text-gray-900 bg-transparent border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer',
                'placeholder':' ',
            }
        ))
    last_name = forms.CharField(max_length=150, required=False,
        widget=forms.TextInput(
            attrs={
                'class':'block py-2.5 px-0 w-full text-sm text-gray-900 bg-transparent border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer',
                'placeholder':' ',
            }
        ))
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