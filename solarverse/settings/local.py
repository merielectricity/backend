from .base import *

SECRET_KEY = os.environ.get(
    "SECRET_KEY", "django-insecure-nu1=)-c9o-&kpc9yir4c42j^tlic1)g31=^it=2b1_s_*piy3+"
)

DEBUG = os.environ.get("DEBUG_VALUE", True)

ALLOWED_HOSTS = []

CORS_ORIGIN_WHITELIST = (
    "http://localhost:3000",
    "*",
)

INSTALLED_APPS += [
    "django_extensions",
    "django_otp",
    "django_otp.plugins.otp_totp",
]

DATABASES = {
    "default": {
        "ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.environ.get("SQL_DATABASE", os.path.join(BASE_DIR, "db.sqlite3")),
        "USER": os.environ.get("SQL_USER", ""),
        "PASSWORD": os.environ.get("SQL_PASSWORD", ""),
        "HOST": os.environ.get("SQL_HOST", ""),
        "PORT": os.environ.get("SQL_PORT", ""),
        "ATOMIC_REQUESTS": True,
    }
}

OSCARAPI_BLOCK_ADMIN_API_ACCESS = False
