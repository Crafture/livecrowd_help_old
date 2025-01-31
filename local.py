from .base import *
ROOT_URLCONF = "config.urls.local_urls"
# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
ALLOWED_HOSTS = ['*',]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'livecrowdfaq',
        'USER': 'livecrowdfaq',
        'PASSWORD': 'LCfaq2018',
    }
}

INSTALLED_APPS += [
    'venues',
    'events',
    'questions',
    'import_export',
]