from .base import *

SECRET_KEY = os.environ.get("SECRET_KEY", "staggingmerielectricty")

DEBUG = os.environ.get("DEBUG_VALUE", True)

INSTALLED_APPS += [
    "django_extensions",
]

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
