from django.urls import path
from .views import TournamentView, UserView

urlpatterns = [
    path('users/', UserView.as_view(), name='users'),
    path('tournament/', TournamentView.as_view(), name='tournament'),
    path('tournament/<int:tournament_id>', TournamentView.as_view(), name='tournament'),
]

