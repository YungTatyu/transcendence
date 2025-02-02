from django.urls import path

from .views import (
    MatchHistoryView,
    MatchView,
    health_check,
)

urlpatterns = [
    path("matches/", MatchView.as_view(), name="matches"),
    path(
        "matches/histories/<str:user_id>/",
        MatchHistoryView.as_view(),
        name="history",
    ),
    path("health", health_check, name="health"),
]
