from .base import *

SECRET_KEY = os.environ.get('SECRET_KEY','solar')

DEBUG = os.environ.get('DEBUG_VALUE', False)

ALLOWED_HOSTS = ["*"]

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('SQL_ENGINE'),
        'NAME': os.environ.get('SQL_DATABASE'),
        'USER': os.environ.get('SQL_USER'),
        'PASSWORD': os.environ.get('SQL_PASSWORD'),
        'HOST': os.environ.get('SQL_HOST'),
        'PORT': os.environ.get('SQL_PORT'),
        'ATOMIC_REQUESTS': True,
    }
}

#SECURE_SSL_REDIRECT = True

#SESSION_COOKIE_SECURE = True

#CSRF_COOKIE_SECURE = True

#SECURE_BROWSER_XSS_FILTER = True