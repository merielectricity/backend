"""
ASGI config for solarverse project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
import dotenv

dotenv.load_dotenv(f".env/{os.environ.get('DJANGO_ENV', 'local')}")


os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    f"solarverse.settings.{os.environ.get('DJANGO_ENV','local')}",
)

application = get_asgi_application()
