from django.urls import path
from .views import RegisterUser, LoginUser, FriendRequestView, FriendRequestActionView

urlpatterns = [
    path("register/", RegisterUser.as_view(), name="register"),
    path("login/", LoginUser.as_view(), name="login"),
    path("friend-requests/", FriendRequestView.as_view(), name="friend_request"),
    path(
        "friend-requests/<int:pk>/",
        FriendRequestActionView.as_view(),
        name="friend_request_action",
    ),
]
