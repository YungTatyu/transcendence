from django.urls import path
from . import views

urlpatterns = [
    path('secure/', views.get, name='secure'),
]