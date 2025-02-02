from django.urls import path

from .views import (
    MatchFinishView,
    MatchStatisticView,
    TournamentMatchView,
    health_check,
)

urlpatterns = [
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
    path("health", health_check, name="health"),
]
