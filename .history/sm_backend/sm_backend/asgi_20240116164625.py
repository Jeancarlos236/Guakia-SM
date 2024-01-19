# asgi.py
import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from chat.Testconsumer import ChatConsumer
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sm_backend.settings')
application = ProtocolTypeRouter(
    {
        # "websocket": AuthMiddlewareStack(
        #     URLRouter(
        #         [
        #             path("ws/chat/<id>/", ChatConsumer.as_asgi()),
        #         ]
        #     )
        # ),
        "http": get_asgi_application(),
        # ... other routing configurations
    }
)
