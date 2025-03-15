from django.urls import re_path

from match_app.consumers.quick_play_consumer import QuickPlayConsumer

websocket_urlpatterns = [
    re_path(r"^matches/ws/enter-room$", QuickPlayConsumer.as_asgi()),
]
