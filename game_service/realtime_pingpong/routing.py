from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(
        r"games/ws/enter-room/(?P<match_id>\d+)$",  # \d+ で数字のみを許容
        consumers.GameConsumer.as_asgi(),
    ),
    # TODO このエンドポイントは動作確認用
    # jwt認証機能が追加されたら削除する
    re_path(
        r"games/ws/enter-room/(?P<match_id>\d+)/(?P<user_id>[a-zA-Z0-9]+)$",
        consumers.GameConsumer.as_asgi(),
    ),
]
