from django.urls import re_path

from tournament_app.consumers.tournament_matching_consumer import (
    TournamentMatchingConsumer,
)
from tournament_app.consumers.tournament_consumer import TournamentConsumer

websocket_urlpatterns = [
    re_path(r"^tournaments/ws/enter-room$", TournamentMatchingConsumer.as_asgi()),
    re_path(
        r"^tournaments/ws/enter-room/(?P<tournamentId>\d+)$",
        TournamentConsumer.as_asgi(),
    ),
]
