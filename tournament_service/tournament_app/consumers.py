from channels.generic.websocket import AsyncWebsocketConsumer
import json
import asyncio
from .utils.tournament_matching_manager import TournamentMatchingManager


class TournamentMatchingConsumer(AsyncWebsocketConsumer):
    # マッチングルームは全てのユーザーが同じルームを使用するので定数を使用
    __matching_room = "matching_room"
    __forced_start_time = 10
    __room_capacity = 4

    # TODO userIdごとにredis上にCounterを作成し、不正ができないようにする
    async def connect(self):
        # Channelにクライアントを登録
        await self.channel_layer.group_add(self.__matching_room, self.channel_name)
        # WebSocket接続を受け入れる
        await self.accept()
        count = TournamentMatchingManager.append_matching_wait_users(self.channel_name)

        # 1 -> 2人のタイミングでトーナメント強制開始タイマーをセット
        if count == 2:
            TournamentMatchingManager.set_timer(
                asyncio.create_task(self.__start_tournament(self.__forced_start_time))
            )

        # マッチング待ちユーザー数がトーナメントの最大参加者人数に達した
        if count == self.__room_capacity:
            TournamentMatchingManager.cancel_timer()
            await self.__start_tournament()

    async def disconnect(self, _):
        await self.channel_layer.group_discard(self.__matching_room, self.channel_name)
        count = TournamentMatchingManager.del_matching_wait_user(self.channel_name)

        # 2 -> 1人のタイミングでトーナメント強制開始タイマーを削除
        if count == 1:
            TournamentMatchingManager.cancel_timer()

    async def __start_tournament(self, delay=0):
        await asyncio.sleep(delay)
        await self.channel_layer.group_send(
            self.__matching_room,
            {"type": "send.tournament.start.message", "message": "START"},
        )
        for user_id in TournamentMatchingManager.get_matching_wait_users():
            await self.channel_layer.group_discard(self.__matching_room, user_id)
        TournamentMatchingManager.clear_matching_wait_users()

    async def send_tournament_start_message(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))
