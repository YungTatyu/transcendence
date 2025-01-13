from channels.generic.websocket import AsyncWebsocketConsumer
import json
from tournament_app.utils.redis_handler import RedisHandler


class TournamentMatchingConsumer(AsyncWebsocketConsumer):
    # マッチングルームは全てのユーザーが同じルームを使用するので定数を使用
    __matching_room = "matching_room"

    async def connect(self):
        # Channelにクライアントを登録
        await self.channel_layer.group_add(self.__matching_room, self.channel_name)
        # WebSocket接続を受け入れる
        await self.accept()
        await self.increment_member_count()

    async def disconnect(self, close_code):
        _ = close_code
        await self.channel_layer.group_discard(self.__matching_room, self.channel_name)
        await self.decrement_member_count()

    async def tournament_start(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))

    async def increment_member_count(self):
        key = f"{self.__matching_room}_count"
        current_count = RedisHandler.get(key=key) or 0
        current_count += 1
        RedisHandler.set(key=key, value=current_count)

        # 参加者がN人になったらメッセージを送る
        if current_count >= 3:
            await self.channel_layer.group_send(
                self.__matching_room, {"type": "tournament.start", "message": "START"}
            )

    async def decrement_member_count(self):
        key = f"{self.__matching_room}_count"
        current_count = RedisHandler.get(key=key) or 0
        current_count -= 1
        RedisHandler.set(key=key, value=current_count)
