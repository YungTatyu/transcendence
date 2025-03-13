import json

from django.conf import settings
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from match_app.utils.quick_play_matching_manager import QuickPlayMatchingManager
from match_app.models import Match, MatchParticipant
from match_app.client.game_client import GameClient


class QuickPlayConsumer(AsyncWebsocketConsumer):
    MATCHING_ROOM = "matching_room"
    ROOM_CAPACITY = 2

    async def connect(self):
        self.user_id = self.scope.get("user_id")
        if not self.user_id:
            await self.close()
            return

        # INFO すでに同じユーザーがマッチングルームにいる場合、接続を拒否する
        if self.user_id in QuickPlayMatchingManager.get_waiting_users():
            await self.close()
            return

        await self.accept()

        lock = await QuickPlayMatchingManager.get_lock()
        async with lock:
            await self.channel_layer.group_add(self.MATCHING_ROOM, self.channel_name)
            count = QuickPlayMatchingManager.add_user(self.user_id, self.channel_name)

            # マッチング待ちユーザー数がQuickPlayの最大参加者人数に達した
            if count == self.ROOM_CAPACITY:
                await self.__start_quick_play()

    async def disconnect(self, _):
        lock = await QuickPlayMatchingManager.get_lock()
        async with lock:
            await self.channel_layer.group_discard(
                self.MATCHING_ROOM, self.channel_name
            )

    async def __start_quick_play(self):
        user_ids = list(QuickPlayMatchingManager.get_waiting_users().keys())
        match_id = await self.__create_quick_play_match(user_ids)
        client = GameClient(settings.GAME_API_BASE_URL)
        res_data = await client.fetch_games(match_id, user_ids)
        if res_data.get("error", None) is not None:
            # 試合レコードと試合参加者レコードを削除
            # Match.objects.filter(match_id=match_id).delete()
            # MatchParticipant.objects.filter(match_id=match_id).delete()
            match_id = None

        await self.channel_layer.group_send(
            self.MATCHING_ROOM,
            {
                "type": "send_quick_play_start_message",
                "match_id": str(match_id),
            },
        )
        for channel_name in QuickPlayMatchingManager.get_waiting_users().values():
            await self.channel_layer.group_discard(self.MATCHING_ROOM, channel_name)
        QuickPlayMatchingManager.clear_waiting_users()

    async def send_quick_play_start_message(self, event):
        match_id = event["match_id"]
        await self.send(text_data=json.dumps({"match_id": match_id}))

    @database_sync_to_async
    def __create_quick_play_match(self, user_ids: list[int]) -> int:
        """
        試合レコードと試合参加者レコードを作成
        """
        match = Match.objects.create(mode="QuickPlay")

        for user_id in user_ids:
            MatchParticipant.objects.create(match_id=match, user_id=user_id)
        return match.match_id
