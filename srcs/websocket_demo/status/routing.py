from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/active_users/$', consumers.ActiveUserConsumer.as_asgi()),
]
