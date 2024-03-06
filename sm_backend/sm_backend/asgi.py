# asgi.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sm_backend.settings')
django.setup()

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from chat.consumers import ChatConsumer
from django.core.asgi import get_asgi_application



application = ProtocolTypeRouter(
    {
        "websocket": AuthMiddlewareStack(
            URLRouter(
                [
                    path("ws/chat/<id>/", ChatConsumer.as_asgi()),
                ]
            )
        ),
        "http": get_asgi_application(),
        # ... other routing configurations
    }
)
