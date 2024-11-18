"""
URL configuration for notes_bonus project.

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
from rest_framework import routers
from notes import views

router = routers.DefaultRouter()
router.register(r"users", views.UserViewSet)
router.register(r"notes", views.NoteViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.NoteListView.as_view(), name="note_list"),
    path("notes/", views.NoteListView.as_view(), name="note_list"),
    path("notes/<int:id>/", views.NoteDetailView.as_view(), name="note_detail"),
    path("notes/create/", views.NoteCreateView.as_view(), name="note_create"),
    path("notes/delete/<int:pk>/", views.NoteDestroyView.as_view(), name="note_delete"),
    path("users/", views.UserListView.as_view(), name="user_list"),
    path("users/create/", views.UserCreateView.as_view(), name="user_create"),
    path("users/delete/<int:pk>/", views.UserDestroyView.as_view(), name="user_delete"),
    path("users/login/", views.UserLoginView.as_view(), name="user_login"),
    path("users/logout/", views.LogoutView.as_view(), name="user_logout"),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
