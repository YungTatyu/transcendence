from django.urls import path
from friends_activity_app import views

urlpatterns = [
    path('health/', views.health_check, name='health-check'),
]
