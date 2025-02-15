import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from friends_activity_app.routing import websocket_urlpatterns
from django.urls import path
from friends_activity_app.views import health_check

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'friends_activity_app.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
