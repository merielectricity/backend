"""
WSGI config for solarverse project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os
import dotenv

from django.core.wsgi import get_wsgi_application
import dotenv

dotenv.load_dotenv(f".env/{os.environ.get('DJANGO_ENV', 'local')}")


os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    f"solarverse.settings.{os.environ.get('DJANGO_ENV','local')}",
)

if os.getenv("DJANGO_SETTINGS_MODULE"):
    os.environ["DJANGO_SETTINGS_MODULE"] = os.getenv("DJANGO_SETTINGS_MODULE")

application = get_wsgi_application()
