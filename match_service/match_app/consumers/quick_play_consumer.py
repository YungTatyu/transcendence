import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings
from match_app.client.game_client import GameClient
from match_app.models import Match, MatchParticipant
from match_app.utils.quick_play_matching_manager import QuickPlayMatchingManager


class QuickPlayConsumer(AsyncWebsocketConsumer):
    """QuickPlayモードのマッチング処理を行うConsumer"""

    MATCHING_ROOM = "matching_room"
    ROOM_CAPACITY = 2

    async def connect(self):
        self.user_id = self.scope.get("user_id")
        if not self.user_id:
            await self.close()
            return

        lock = await QuickPlayMatchingManager.get_lock()
        async with lock:
            waiting_user_ids = list(QuickPlayMatchingManager.get_waiting_users().keys())

            # INFO すでに同じユーザーがマッチングルームにいる場合、接続を拒否する
            if self.user_id in waiting_user_ids:
                await self.close()
                return

            selected_protocol = self.scope.get("subprotocol")
            await self.accept(subprotocol=selected_protocol)

            await self.channel_layer.group_add(self.MATCHING_ROOM, self.channel_name)
            count = QuickPlayMatchingManager.add_user(self.user_id, self.channel_name)

            # マッチング待ちユーザー数がQuickPlayの最大参加者人数に達した
            if count == self.ROOM_CAPACITY:
                await self.__start_quick_play()
            else:
                user_ids = list(QuickPlayMatchingManager.get_waiting_users().keys())
                await self.channel_layer.group_send(
                    self.MATCHING_ROOM,
                    {
                        "type": "send_quick_play_start_message",
                        "user_id_list": user_ids,
                    },
                )

    async def disconnect(self, _):
        lock = await QuickPlayMatchingManager.get_lock()
        async with lock:
            await self.channel_layer.group_discard(
                self.MATCHING_ROOM, self.channel_name
            )
            users = QuickPlayMatchingManager.get_waiting_users()
            if users.get(self.user_id, None) and users[self.user_id] == self.channel_name:
                QuickPlayMatchingManager.del_user(self.user_id)
            user_ids = list(QuickPlayMatchingManager.get_waiting_users().keys())
            await self.channel_layer.group_send(
                self.MATCHING_ROOM,
                {
                    "type": "send_quick_play_start_message",
                    "user_id_list": user_ids,
                },
            )

    async def __start_quick_play(self):
        user_ids = list(QuickPlayMatchingManager.get_waiting_users().keys())
        match_id = await self.__create_quick_play_match(user_ids)

        # GameAPIを叩き、ゲーム開始の準備を行う
        client = GameClient(settings.GAME_API_BASE_URL)
        res_data = await client.fetch_games(match_id, user_ids)
        if res_data.get("error", None) is not None:
            # INFO 非同期関数なのでDjangoのトランザクション処理は難しそうでした
            await self.__rollback_quick_play_match(match_id)
            # INFO 内部エラーが起きたときはユーザーに`match_id: "None"`を返す
            match_id = None

        await self.channel_layer.group_send(
            self.MATCHING_ROOM,
            {
                "type": "send_quick_play_start_message",
                "match_id": str(match_id),
                "user_id_list": user_ids,
            },
        )
        for channel_name in QuickPlayMatchingManager.get_waiting_users().values():
            await self.channel_layer.group_discard(self.MATCHING_ROOM, channel_name)
        QuickPlayMatchingManager.clear_waiting_users()

    async def send_quick_play_start_message(self, event):
        data = {}
        if event.get("match_id", None) is not None:
            data["match_id"] = event["match_id"]
        data["user_id_list"] = event["user_id_list"]
        await self.send(text_data=json.dumps(data))

    @database_sync_to_async
    def __create_quick_play_match(self, user_ids: list[int]) -> int:
        """
        試合レコードと試合参加者レコードを作成
        """
        match = Match.objects.create(mode="QuickPlay")

        for user_id in user_ids:
            MatchParticipant.objects.create(match_id=match, user_id=user_id)
        return match.match_id

    @database_sync_to_async
    def __rollback_quick_play_match(self, match_id: int):
        """
        __create_quick_play_matchで作成したレコードを削除する処理
        """
        Match.objects.filter(match_id=match_id).delete()
        MatchParticipant.objects.filter(match_id=match_id).delete()
