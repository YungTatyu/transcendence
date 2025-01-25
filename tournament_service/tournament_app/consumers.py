import json
from typing import Optional

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from tournament_app.models import Tournaments

from .utils.tournament_matching_manager import TournamentMatchingManager
from .utils.tournament_session import TournamentSession


class TournamentMatchingConsumer(AsyncWebsocketConsumer):
    """
    トーナメントマッチング用WebSocketを管理する
    マッチングは条件1, 2のいずれかを満たすと完了する
        1. マッチング待機ユーザーが1 -> 2人になったタイミングで
           FORCED_START_TIME秒でセットされる
           トーナメント強制開始タイマーが0秒となった
           (トーナメント開始 OR 2 -> 1人になるタイミングで強制開始タイマーは削除)
        2. マッチング待機ユーザー数がROOM_CAPACITYに達した
    """

    # マッチングルームは全てのユーザーが同じルームを使用するので定数を使用
    MATCHING_ROOM = "matching_room"
    FORCED_START_TIME = 10
    ROOM_CAPACITY = 4

    # TODO self.scope["client"][1] -> userId(現状はuserIdではなく、ポート番号の値を使用)
    async def connect(self):
        # 既にマッチング待機中なら接続を拒否する
        if self.scope["client"][1] in TournamentMatchingManager.get_waiting_users():
            await self.close(code=4400)
            return

        await self.accept()

        # Lockを用いて1人ずつ処理(パフォーマンスを犠牲に整合性を保つ)
        async with TournamentMatchingManager.get_lock():
            await self.channel_layer.group_add(self.MATCHING_ROOM, self.channel_name)
            count = TournamentMatchingManager.add_user(
                self.scope["client"][1], self.channel_name
            )

            # 1 -> 2人のタイミングでトーナメント強制開始タイマーをセット
            if count == 2:
                TournamentMatchingManager.set_task(
                    self.FORCED_START_TIME, self.__start_tournament
                )

            # 新規ユーザー接続時にルーム内のユーザーにマッチングルームの状態をSend
            execution_time = TournamentMatchingManager.get_task_execution_time()
            wait_user_ids = list(TournamentMatchingManager.get_waiting_users().keys())
            await self.__broadcast_matching_room_state(execution_time, wait_user_ids)

            # マッチング待ちユーザー数がトーナメントの最大参加者人数に達した
            if count == self.ROOM_CAPACITY:
                await self.__start_tournament()

    async def disconnect(self, _):
        async with TournamentMatchingManager.get_lock():
            await self.channel_layer.group_discard(
                self.MATCHING_ROOM, self.channel_name
            )
            count = TournamentMatchingManager.del_user(self.scope["client"][1])

            # 2 -> 1人のタイミングでトーナメント強制開始タイマーを解除
            if count == 1:
                TournamentMatchingManager.cancel_task()
                wait_user_ids = list(
                    TournamentMatchingManager.get_waiting_users().keys()
                )
                await self.__broadcast_matching_room_state(None, wait_user_ids)

    async def __broadcast_matching_room_state(
        self, start_time: Optional[float], wait_user_ids: list[int]
    ):
        """
        マッチング待機中のユーザーにトーナメント強制開始時刻と待機中ユーザーのIDをSend
        1人しか待機していない場合、強制開始タイマーはセットされていないことをNoneで伝える
        """
        await self.channel_layer.group_send(
            self.MATCHING_ROOM,
            {
                "type": "send.matching.room.state",
                "tournament_start_time": str(start_time),
                "wait_user_ids": str(wait_user_ids),
            },
        )

    async def __start_tournament(self):
        """
        1. リソースを作成
        2. tournament_id Send
        3. ユーザーをchannelから削除
        4. タイマーを削除(タスクがない場合は何もしない)
        """
        tournament_id = await self.__create_tournament()
        await self.channel_layer.group_send(
            self.MATCHING_ROOM,
            {
                "type": "send.tournament.start.message",
                "tournament_id": str(tournament_id),
            },
        )
        for channel_name in TournamentMatchingManager.get_waiting_users().values():
            await self.channel_layer.group_discard(self.MATCHING_ROOM, channel_name)
        TournamentMatchingManager.clear_waiting_users()
        TournamentMatchingManager.cancel_task()

    async def send_tournament_start_message(self, event):
        tournament_id = event["tournament_id"]
        await self.send(text_data=json.dumps({"tournament_id": tournament_id}))

    async def send_matching_room_state(self, event):
        start_time = event["tournament_start_time"]
        wait_user_ids = event["wait_user_ids"]
        await self.send(
            text_data=json.dumps(
                {
                    "tournament_start_time": start_time,
                    "wait_user_ids": wait_user_ids,
                }
            )
        )

    @database_sync_to_async
    def __create_tournament(self) -> int:
        """永続的データとメモリ上のデータの両方を作成"""
        tournament = Tournaments.objects.create()
        tournament_id = tournament.tournament_id
        TournamentSession.register(
            tournament_id,
            list(TournamentMatchingManager.get_waiting_users().keys()),
        )
        return tournament_id
