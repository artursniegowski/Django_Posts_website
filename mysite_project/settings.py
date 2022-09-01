"""
Django settings for mysite_project project.

Generated by 'django-admin startproject' using Django 4.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os

################################
# just for your local machine !!
# NOT NEEDED IN PRODUCTION
from dotenv import load_dotenv
load_dotenv()
#################################

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# BASE_DIR same as PROJECT_DIR
# PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Meddia served for non - production
# URL that handles the media served from MEDIA_ROOT, 
# used for managing stored files. It must end in a slash if set to a non-empty 
# value. You will need to configure these files to be served in both development 
# and production environments
MEDIA_URL = 'media/'
# Absolute filesystem path to the directory that will hold user-uploaded files.
MEDIA_ROOT = BASE_DIR / MEDIA_URL


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    ## added
    # third party
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'django.contrib.sites',
    'sorl.thumbnail',

    # own apps
    'feed_app.apps.FeedAppConfig',  # 'feed_app',
    'profiles_app.apps.ProfilesAppConfig', # 'profiles_app',
    'followers_app.apps.FollowersAppConfig', # 'followers_app',

    ## default
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mysite_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
            # or if we move templates to our mysite_project
            # BASE_DIR / 'mysite_project/templates',
            # os.path.join(PROJECT_DIR, 'mysite_project/templates')
            ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mysite_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static_frontend',
    # BASE_DIR / 'static', # for production , after running collectstatic
]
# for python manage.py collectstatic - where to move static files
# for PRODUCTION we shoudl move the files !
STATIC_ROOT = BASE_DIR / 'static'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# for allauth settings
# https://django-allauth.readthedocs.io/en/latest/installation.html
# Now start your server, visit your admin pages (e.g. http://localhost:8000/admin/) 
# and follow these steps:
# Add a Site for your domain, matching settings.SITE_ID (django.contrib.sites app).
# Add your site name and domail in admin site (/admin/sites/site/) 
# and replace SITE_ID with your sites pk.
SITE_ID = 2 # currently the id in the database of the site is , id = 2

AUTHENTICATION_BACKENDS = [
    
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
    
]

# for allauth
# Specifies the login method to use – whether the user logs in by entering 
# their username, e-mail address, or either one of both. 
# Setting this to “email” requires ACCOUNT_EMAIL_REQUIRED=True
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_AUTHENTICATION_METHOD = "email"
# The user is required to hand over an e-mail address when signing up.
ACCOUNT_EMAIL_REQUIRED = True
# Determines whether or not an e-mail address is automatically confirmed by a GET request.
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
# Determines the e-mail verification method during signup – choose one of "mandatory", "optional", or "none".
# Setting this to “mandatory” requires ACCOUNT_EMAIL_REQUIRED to be True
# When set to “mandatory” the user is blocked from logging in until the email 
# address is verified. Choose “optional” or “none” to allow logins 
# with an unverified e-mail address. In case of “optional”, 
# the e-mail verification mail is still sent, whereas in case of 
# “none” no e-mail verification mails are sent.
ACCOUNT_EMAIL_VERIFICATION = "optional"
# The default behaviour is not log users in and to redirect them to 
# ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL.
# By changing this setting to True, users will automatically be logged in 
# once they confirm their email address. Note however that this only works 
# when confirming the email address immediately after signing up, 
# assuming users didn’t close their browser or used some sort of private browsing mode.
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
# Determines whether or not the user is automatically logged out by a GET request. 
# GET is not designed to modify the server state, and in this case it can be dangerous. 
# See LogoutView in the documentation for details.
ACCOUNT_LOGOUT_ON_GET = True
# By changing this setting to True, users will automatically be logged in once 
# they have reset their password. By default they are redirected 
# to the password reset done page.
ACCOUNT_LOGIN_ON_PASSWORD_RESET = True
# The URL (or URL name) to return to after the user logs out. 
# Defaults to Django’s LOGOUT_REDIRECT_URL, unless that is empty, then “/” is used
ACCOUNT_LOGOUT_REDIRECT_URL = '/' # back to home page
# This setting determines whether the username is stored in lowercase (False) 
# or whether its casing is to be preserved (True). Note that when casing is preserved, 
# potentially expensive __iexact lookups are performed when filter on username. 
# For now, the default is set to True to maintain backwards compatibility.
ACCOUNT_PRESERVE_USERNAME_CASING = False
# Controls the life time of the session. Set to None to ask the user 
# (“Remember me?”), False to not remember, and True to always remember.
ACCOUNT_SESSION_REMEMBER = True
# When signing up, let the user type in their password twice to avoid typos.
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = True 
# An integer specifying the minimum allowed length of a username.
ACCOUNT_USERNAME_MIN_LENGTH = 3


# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# This backend is not intended for use in production – it is provided as a convenience that can be used during development.
# nstead of sending out real emails the console backend just writes the emails that would be sent to the standard output.
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# default login url
# The URL or named URL pattern where requests are redirected 
# for login when using the login_required() decorator, 
# LoginRequiredMixin, or AccessMixin.
LOGIN_URL = '/login/'

# The URL or named URL pattern where requests are redirected after login 
# when the LoginView doesn’t get a next GET parameter.
LOGIN_REDIRECT_URL = '/' # home page for now