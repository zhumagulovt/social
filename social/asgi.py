"""
ASGI config for social project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter

# from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator

from chat import routing

from .channelsmiddleware import JWTAuthMiddlewareStack

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "social.settings")

application = ProtocolTypeRouter(
    {
        # Websocket чат
        "websocket": AllowedHostsOriginValidator(  # Only allow socket connections from the Allowed hosts in the settings.py file
            JWTAuthMiddlewareStack(  # Кастомная JWT авторизация
                URLRouter(routing.websocket_urlpatterns)
            ),
        ),
    }
)
