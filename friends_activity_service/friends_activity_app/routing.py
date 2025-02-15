from django.urls import path
from friends_activity_app import consumers

websocket_urlpatterns = [
    path(r"friends/online/", consumers.LoggedInUsersConsumer.as_asgi()),
]
