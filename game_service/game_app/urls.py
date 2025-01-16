from django.urls import path
from core import views

urlpatterns = [
    path("games", views.GameView.as_view(), name="games"),
    path("health", views.health_check, name="health"),
]
