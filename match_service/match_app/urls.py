from django.urls import path

from .views import (
    MatchFinishView,
    MatchHistoryView,
    MatchStatisticView,
    MatchView,
    TournamentMatchView,
    health_check,
)

urlpatterns = [
    path("matches/", MatchView.as_view(), name="matches"),
    path(
        "matches/tournament-match/",
        TournamentMatchView.as_view(),
        name="tournament-match",
    ),
    path("matches/finish/", MatchFinishView.as_view(), name="finish"),
    path(
        "matches/statistics/<str:user_id>/",
        MatchStatisticView.as_view(),
        name="statistic",
    ),
    path(
        "matches/histories/<str:user_id>/",
        MatchHistoryView.as_view(),
        name="history",
    ),
    path("health", health_check, name="health"),
]
