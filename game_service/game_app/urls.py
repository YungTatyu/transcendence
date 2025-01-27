from core import views
from django.urls import path

urlpatterns = [
    path("games", views.GameView.as_view(), name="games"),
    path("health", views.health_check, name="health"),
]
