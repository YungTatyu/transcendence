from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"^tournaments/ws/enter-room$", consumers.TournamentConsumer.as_asgi()),
]
