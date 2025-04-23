from django.urls import include, path

from .views import health_check

urlpatterns = [
    path("health", health_check, name="health-check"),
    path('', include('django_prometheus.urls')),
]
