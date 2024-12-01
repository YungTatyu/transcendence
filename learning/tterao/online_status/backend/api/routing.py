from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path("status/", consumers.UserStatusConsumer.as_asgi()),
]
