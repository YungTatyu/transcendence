from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(
        r"games/ws/enter-room/(?P<matchId>\d+)$",  # \d+ で数字のみを許容
        consumers.GameConsumer.as_asgi(),
    ),
    # TODO このエンドポイントは動作確認用
    # jwt認証機能が追加されたら削除する
    re_path(
        r"games/ws/enter-room/(?P<matchId>\d+)/(?P<userId>\d+)$",
        consumers.GameConsumer.as_asgi(),
    ),
]
