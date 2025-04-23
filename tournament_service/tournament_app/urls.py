from django.urls import include, path

from .views import TournamentMatchFinishView, health_check

urlpatterns = [
    path("health", health_check, name="health"),
    path(
        "tournaments/finish-match",
        TournamentMatchFinishView.as_view(),
        name="finish_match",
    ),
    path('', include('django_prometheus.urls')),
]
