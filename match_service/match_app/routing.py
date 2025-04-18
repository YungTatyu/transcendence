from django.urls import re_path

from match_app.consumers.quick_play_consumer import QuickPlayConsumer
from match_app.consumers.tournament_match_consumer import TournamentMatchConsumer

websocket_urlpatterns = [
    re_path(r"^matches/ws/enter-room$", QuickPlayConsumer.as_asgi()),
    re_path(
        r"^matches/ws/enter-room/(?P<matchId>\d+)$",
        TournamentMatchConsumer.as_asgi(),
    ),
]
