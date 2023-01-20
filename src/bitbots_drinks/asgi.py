"""
ASGI config for bitbots_drinks project.

It exposes the ASGI callable as a module-level variable named ``app``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bitbots_drinks.settings")
app = get_asgi_application()
