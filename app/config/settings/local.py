from .base import *
ROOT_URLCONF = "config.urls.local_urls"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
ALLOWED_HOSTS = ['*',]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['LCFAQ_DB_NAME'],
        'USER': os.environ['LCFAQ_DB_USER'],
        'PASSWORD': os.environ['LCFAQ_DB_PASSWORD'],
    }
}

INSTALLED_APPS += [

]