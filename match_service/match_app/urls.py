from django.urls import path

from match_app.views.health_check import health_check
from match_app.views.match_view import MatchView
from match_app.views.match_history_view import MatchHistoryView

urlpatterns = [
    path("matches/", MatchView.as_view(), name="matches"),
    path(
        "matches/histories/<str:user_id>/",
        MatchHistoryView.as_view(),
        name="history",
    ),
    path("health", health_check, name="health"),
]
