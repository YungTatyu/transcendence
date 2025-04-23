from django.urls import include, path

from match_app.views.health_check import health_check
from match_app.views.match_finish_view import MatchFinishView
from match_app.views.match_history_view import MatchHistoryView
from match_app.views.match_statistic_view import MatchStatisticView
from match_app.views.match_view import MatchView
from match_app.views.tournament_match_view import TournamentMatchView

urlpatterns = [
    path("matches", MatchView.as_view(), name="matches"),
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
    path(
        "matches/histories/<str:user_id>",
        MatchHistoryView.as_view(),
        name="history",
    ),
    path("health", health_check, name="health"),
    path("", include("django_prometheus.urls")),
]
