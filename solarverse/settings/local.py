from .base import *

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-nu1=)-c9o-&kpc9yir4c42j^tlic1)g31=^it=2b1_s_*piy3+')

DEBUG = os.environ.get('SECRET_KEY', True)

ALLOWED_HOSTS = []

CORS_ORIGIN_WHITELIST = (
    'http://localhost:3000',
    '*',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
        'ATOMIC_REQUESTS': True,
    }
}