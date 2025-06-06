"""
URL configuration for user_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path

from .views import AvatarView, UsernameView, UserView, health_check

urlpatterns = [
    path("admin", admin.site.urls),
    path("health", health_check, name="health"),
    path("users", UserView.as_view(), name="users"),
    path("users/me/username", UsernameView.as_view(), name="update-username"),
    path("users/me/avatar", AvatarView.as_view(), name="update-avatar"),
    path("", include("django_prometheus.urls")),
]
