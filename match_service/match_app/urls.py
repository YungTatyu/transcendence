from django.urls import path
import views

urlpatterns = [
    path("matches/", views.MatchView.as_view(), name="matches"),
    path(
        "matches/tournament-match/",
        views.TournamentMatchView.as_view(),
        name="tournament-match",
    ),
    path("matches/finish/", views.MatchFinishView.as_view(), name="finish"),
    path(
        "matches/statistics/<int:user_id>/",
        views.MatchStatisticView.as_view(),
        name="statistic",
    ),
    path(
        "matches/histories/<int:user_id>/",
        views.MatchHistoryView.as_view(),
        name="history",
    ),
    path("health", views.health_check, name="health"),
]
