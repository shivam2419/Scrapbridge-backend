from pathlib import Path
import os
from decouple import config


SECRET_KEY = ""
GOOGLE_CLIENT_ID = ""
GOOGLE_CLIENT_SECRET = ""
RAZORPAY_API_KEY = ""
RAZORPAY_API_SECRET_KEY = ""
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = ""
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = ""

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


SITE_ID = 1  # Required for django-allauth
# Application definition
INSTALLED_APPS = [
    'django.contrib.sites',  # Required for django-allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',  # Google OAuth Provider
    'dj_rest_auth',
    'dj_rest_auth.registration',
    'rest_framework',
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'rest_framework.authtoken',
    'django.contrib.staticfiles',
    'social_django',
    'myApp',
]
# ASGI_APPLICATION = "EWaste.asgi.application"
# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "channels.layers.InMemoryChannelLayer",  # Use Redis in production
#     },
# }
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP' : {
            'client_id' : GOOGLE_CLIENT_ID,
            'secret' : GOOGLE_CLIENT_SECRET,
            'key' : ''
        },
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
    }
}
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django.middleware.common.CommonMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'EWaste.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join('templates')],
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

WSGI_APPLICATION = 'EWaste.wsgi.application'

CORS_ALLOW_ALL_ORIGINS = True

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Abstract user
# AUTH_USER_MODEL = 'myApp.CustomUser'
# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "static"
]
STATIC_ROOT = BASE_DIR / 'staticfiles'
# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 25-03 changes
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'allauth.account.auth_backends.AuthenticationBackend',  
    'django.contrib.auth.backends.ModelBackend',  # Default Django auth
)
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = SOCIAL_AUTH_GOOGLE_OAUTH2_KEY  # Get this from Google Developer Console
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET

LOGIN_URL = "http://localhost:5173/login/"
LOGOUT_URL = "http://localhost:5173/logout/"
LOGIN_REDIRECT_URL = "http://localhost:5173/login/"
ACCOUNT_LOGOUT_REDIRECT_URL = "http://localhost:5173/login/"

RAZORPAY_API_KEY = RAZORPAY_API_KEY
RAZORPAY_API_SECRET_KEY = RAZORPAY_API_SECRET_KEY