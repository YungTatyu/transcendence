from django.urls import re_path
from friends_activity_app import consumers

websocket_urlpatterns = [
    re_path(r'ws/logged-in-users/', consumers.LoggedInUsersConsumer.as_asgi()),
]
