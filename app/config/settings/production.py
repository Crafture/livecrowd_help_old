from .base import *
ROOT_URLCONF = "config.urls.production_urls"

DEBUG = False

SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
# SET THIS TO TRUE BEFORE DEPLOYING
SECURE_SSL_REDIRECT = True
# SET THIS TO TRUE BEFORE DEPLOYING
SESSION_COOKIE_SECURE = True
# SET THIS TO TRUE BEFORE DEPLOYING
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = 'SAMEORIGIN'
SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
ALLOWED_HOSTS = ['*',]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['LCFAQ_DB_NAME'],
        'USER': os.environ['LCFAQ_DB_USER'],
        'PASSWORD': os.environ['LCFAQ_DB_PASSWORD'],
        'HOST': 'localhost',
    }
}

INSTALLED_APPS += [

]
