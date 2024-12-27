from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"msg/", consumers.gsmeConsumer.as_asgi()),
]
