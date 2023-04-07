from .base import *

SECRET_KEY = os.environ.get("SECRET_KEY", "staggingmerielectricty")

DEBUG = os.environ.get("DEBUG_VALUE", False)

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS += [
     "django_extensions",
]

OSCARAPI_USER_FIELDS = ("first_name","last_name", "email", "phone_number","date_joined","last_login", "is_phone_verified","is_staff","is_active","is_email_verified")

DATABASES = {
    "default": {
        "ENGINE": os.environ.get(
            "SQL_ENGINE", "django.db.backends.postgresql_psycopg2"
        ),
        "NAME": os.environ.get("SQL_DATABASE"),
        "USER": os.environ.get("SQL_USER"),
        "PASSWORD": os.environ.get("SQL_PASSWORD"),
        "HOST": os.environ.get("SQL_HOST"),
        "PORT": os.environ.get("SQL_PORT"),
        "ATOMIC_REQUESTS": True,
    }
}


OSCARAPI_BLOCK_ADMIN_API_ACCESS = False
