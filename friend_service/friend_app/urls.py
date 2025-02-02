from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from .views import FriendRequestView
from .views import FriendView

urlpatterns = [
    path("friends/requests/<str:user_id>/", FriendRequestView.as_view(), name="friend-request"),
	path("friends/<str:friend_id>/", FriendView.as_view(), name="friend"),
]