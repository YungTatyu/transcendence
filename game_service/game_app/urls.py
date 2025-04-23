from core import views
from django.urls import include, path

urlpatterns = [
    path("games", views.GameView.as_view(), name="games"),
    path("health", views.health_check, name="health"),
    path("", include("django_prometheus.urls")),
]
