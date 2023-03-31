from .base import *

SECRET_KEY = os.environ.get('SECRET_KEY','solar')

DEBUG = os.environ.get('DEBUG_VALUE', False)

ALLOWED_HOSTS = ["*"]

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('SQL_ENGINE', 'django.db.backends.postgresql_psycopg2'),
        'NAME': os.environ.get('SQL_DATABASE', 'solardb'),
        'USER': os.environ.get('SQL_USER', 'dbuser'),
        'PASSWORD': os.environ.get('SQL_PASSWORD', 'Qwerty@123'),
        'HOST': os.environ.get('SQL_HOST', 'localhost'),
        'PORT': os.environ.get('SQL_PORT', '5432'),
        'ATOMIC_REQUESTS': True,
    }
}

#SECURE_SSL_REDIRECT = True

#SESSION_COOKIE_SECURE = True

#CSRF_COOKIE_SECURE = True

#SECURE_BROWSER_XSS_FILTER = True
