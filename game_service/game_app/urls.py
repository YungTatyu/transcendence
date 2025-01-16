from django.urls import path
from core import views

urlpatterns = [
    path("games", views.Games.as_view(), name="games"),
    path("health", views.health, name="health"),
]
