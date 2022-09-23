from django.urls import path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    path('', ChatConsumer.as_asgi()) ,
]
