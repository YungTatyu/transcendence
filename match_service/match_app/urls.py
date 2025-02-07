from django.urls import path

from match_app.views.match_finish_view import MatchFinishView
from match_app.views.match_statistic_view import MatchStatisticView
from match_app.views.tournament_match_view import TournamentMatchView
from match_app.views.health_check import health_check

urlpatterns = [
    path(
        "matches/tournament-match",
        TournamentMatchView.as_view(),
        name="tournament-match",
    ),
    path("matches/finish", MatchFinishView.as_view(), name="finish"),
    path(
        "matches/statistics/<str:user_id>",
        MatchStatisticView.as_view(),
        name="statistic",
    ),
    path("health", health_check, name="health"),
]
