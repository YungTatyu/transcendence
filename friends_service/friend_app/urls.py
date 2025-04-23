from django.urls import include, path

from .views import FriendListView, FriendRequestView, FriendView, health_check

urlpatterns = [
    path("friends", FriendListView.as_view(), name="friend-list"),
    path(
        "friends/requests/<str:user_id>",
        FriendRequestView.as_view(),
        name="friend-request",
    ),
    path("friends/<str:friend_id>", FriendView.as_view(), name="friend"),
    path("health", health_check, name="health"),
    path('', include('django_prometheus.urls')),
]
