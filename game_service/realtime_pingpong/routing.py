from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(
        r"games/ws/enter-room/(?P<matchId>\d+)/$",  # \d+ で数字のみを許容
        consumers.ChatConsumer.as_asgi(),
    ),
]
