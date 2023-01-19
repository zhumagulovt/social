"""
ASGI config for social project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

from social.chat import routing

from .channelsmiddleware import JWTAuthMiddlewareStack

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = ProtocolTypeRouter(
    {
        # Websocket chat
        "websocket": AllowedHostsOriginValidator(  # Only allow socket connections from the Allowed hosts in the settings.py file
            JWTAuthMiddlewareStack(  # Custom JWT authorization
                URLRouter(routing.websocket_urlpatterns)
            ),
        ),
    }
)
