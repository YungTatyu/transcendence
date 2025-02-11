from django.urls import path
from friends_activity_app import consumers

websocket_urlpatterns = [
    path(r'ws/logged-in-users/', consumers.LoggedInUsersConsumer.as_asgi()),
]
