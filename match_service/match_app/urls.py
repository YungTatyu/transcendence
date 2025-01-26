from .views import (
    MatchView,
    TournamentMatchView,
    MatchFinishView,
    MatchStatisticView,
    MatchHistoryView,
    health_check,
)
from django.urls import path

urlpatterns = [
    path("matches/", MatchView.as_view(), name="matches"),
    path(
        "matches/tournament-match/",
        TournamentMatchView.as_view(),
        name="tournament-match",
    ),
    path("matches/finish/", MatchFinishView.as_view(), name="finish"),
    path(
        "matches/statistics/<int:user_id>/",
        MatchStatisticView.as_view(),
        name="statistic",
    ),
    path(
        "matches/histories/<int:user_id>/",
        MatchHistoryView.as_view(),
        name="history",
    ),
    path("health", health_check, name="health"),
]
