from typing import Optional
from channels.generic.websocket import AsyncWebsocketConsumer
import json
import asyncio
from .utils.tournament_matching_manager import TournamentMatchingManager
from tournament_app.models import Tournaments
from channels.db import database_sync_to_async
from .utils.tournament_session import TournamentSession


class TournamentMatchingConsumer(AsyncWebsocketConsumer):
    # マッチングルームは全てのユーザーが同じルームを使用するので定数を使用
    __matching_room = "matching_room"
    __forced_start_time = 10
    __room_capacity = 4

    # TODO self.scope["client"][1] -> userId
    async def connect(self):
        # 既にマッチング待機中なら接続を拒否する
        matching_wait_users = TournamentMatchingManager.get_matching_wait_users()
        if self.scope["client"][1] in matching_wait_users:
            await self.close(code=4400)
            return

        await self.channel_layer.group_add(self.__matching_room, self.channel_name)
        await self.accept()
        count = TournamentMatchingManager.add_matching_wait_users(
            self.scope["client"][1], self.channel_name
        )

        # 1 -> 2人のタイミングでトーナメント強制開始タイマーをセット
        if count == 2:
            TournamentMatchingManager.set_task(
                asyncio.create_task(self.__start_tournament(self.__forced_start_time)),
                self.__forced_start_time,
            )

        # マッチング待ちユーザー数がトーナメントの最大参加者人数に達した
        if count == self.__room_capacity:
            await self.__start_tournament()
            return

        # 新規ユーザー接続時にトーナメント強制開始時刻をsend(1人ならNoneをsend)
        execution_time = TournamentMatchingManager.get_task_execution_time()
        await self.__inform_tournament_start_time(execution_time)

    async def disconnect(self, _):
        await self.channel_layer.group_discard(self.__matching_room, self.channel_name)
        count = TournamentMatchingManager.del_matching_wait_user(
            self.scope["client"][1]
        )

        # 2 -> 1人のタイミングでトーナメント強制開始タイマーを解除
        if count == 1:
            TournamentMatchingManager.cancel_task()
            await self.__inform_tournament_start_time(None)

    async def __inform_tournament_start_time(self, start_time: Optional[float]):
        await self.channel_layer.group_send(
            self.__matching_room,
            {
                "type": "send.tournament.start.time",
                "tournament_start_time": str(start_time),
            },
        )

    async def __start_tournament(self, delay=0):
        await asyncio.sleep(delay)
        tournament_id = await self.__create_tournament()
        await self.channel_layer.group_send(
            self.__matching_room,
            {
                "type": "send.tournament.start.message",
                "tournament_id": str(tournament_id),
            },
        )
        matching_wait_users = TournamentMatchingManager.get_matching_wait_users()
        for channel_name in matching_wait_users.values():
            await self.channel_layer.group_discard(self.__matching_room, channel_name)
        TournamentMatchingManager.clear_matching_wait_users()
        TournamentMatchingManager.cancel_task()

    async def send_tournament_start_message(self, event):
        tournament_id = event["tournament_id"]
        await self.send(text_data=json.dumps({"tournament_id": tournament_id}))

    async def send_tournament_start_time(self, event):
        start_time = event["tournament_start_time"]
        await self.send(text_data=json.dumps({"tournament_start_time": start_time}))

    @database_sync_to_async
    def __create_tournament(self) -> int:
        """永続的データとメモリ上のデータの両方を作成"""
        tournament = Tournaments.objects.create()
        tournament_id = tournament.tournament_id
        TournamentSession.register_tournament_session(
            tournament_id,
            list(TournamentMatchingManager.get_matching_wait_users().keys()),
        )
        return tournament_id
