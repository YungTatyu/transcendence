import json
from typing import Optional

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from tournament_app.models import Tournament
from tournament_app.utils.tournament_matching_manager import TournamentMatchingManager
from tournament_app.utils.tournament_session import TournamentSession


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

    async def connect(self):
        if not self.scope.get("user_id"):
            await self.close()
            return

        self.user_id = int(self.scope.get("user_id"))

        # Lockを用いて1人ずつ処理(パフォーマンスを犠牲に整合性を保つ)
        lock = await TournamentMatchingManager.get_lock()
        async with lock:
            wait_user_ids = list(TournamentMatchingManager.get_waiting_users().keys())

            if self.user_id in wait_user_ids:
                await self.close(code=4400)
                return

            selected_protocol = self.scope.get("subprotocol")
            await self.accept(subprotocol=selected_protocol)

            await self.channel_layer.group_add(self.MATCHING_ROOM, self.channel_name)
            count = TournamentMatchingManager.add_user(self.user_id, self.channel_name)

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
        """
        INFO トーナメント開始のタイミングでdisconnectが多発し、
             0 or 1人でトーナメントが開始される可能性があるため、
             connectとdisconnectは同時に処理されないように排他制御しています
        """
        lock = await TournamentMatchingManager.get_lock()
        async with lock:
            await self.channel_layer.group_discard(
                self.MATCHING_ROOM, self.channel_name
            )
            users = TournamentMatchingManager.get_waiting_users()
            if (
                users.get(self.user_id, None)
                and users[self.user_id] == self.channel_name
            ):
                count = TournamentMatchingManager.del_user(self.user_id)

                # 2 -> 1人のタイミングでトーナメント強制開始タイマーを解除
                if count == 1:
                    TournamentMatchingManager.cancel_task()

            wait_user_ids = list(TournamentMatchingManager.get_waiting_users().keys())
            execution_time = TournamentMatchingManager.get_task_execution_time()
            await self.__broadcast_matching_room_state(execution_time, wait_user_ids)

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
                "wait_user_ids": wait_user_ids,
            },
        )

    async def __start_tournament(self):
        """
        1. リソースを作成
        2. tournament_id(TournamentSession作成失敗ならNone)をSend
        3. ユーザーをchannelから削除
        4. タイマーを削除(タスクがない場合は何もしない)
        """
        tournament_id = await self.__create_tournament()
        wait_user_ids = list(TournamentMatchingManager.get_waiting_users().keys())
        await self.channel_layer.group_send(
            self.MATCHING_ROOM,
            {
                "type": "send.matching.room.state",
                "tournament_id": str(tournament_id),
                "tournament_start_time": str(None),
                "wait_user_ids": wait_user_ids,
            },
        )
        for channel_name in TournamentMatchingManager.get_waiting_users().values():
            await self.channel_layer.group_discard(self.MATCHING_ROOM, channel_name)
        TournamentMatchingManager.clear_waiting_users()
        TournamentMatchingManager.cancel_task()

    async def send_matching_room_state(self, event):
        data = {}
        if event.get("tournament_id", None) is not None:
            data["tournament_id"] = event["tournament_id"]
        data["tournament_start_time"] = event["tournament_start_time"]
        data["wait_user_ids"] = event["wait_user_ids"]
        data["room_capacity"] = TournamentMatchingConsumer.ROOM_CAPACITY
        await self.send(text_data=json.dumps(data))

    @database_sync_to_async
    def __create_tournament(self) -> Optional[int]:
        """
        永続的データとメモリ上のデータの両方を作成
        [INFO] TournamentSession.register失敗時、Noneが返る
        """
        tournament = Tournament.objects.create()
        tournament_id = tournament.tournament_id
        session = TournamentSession.register(
            tournament_id,
            list(TournamentMatchingManager.get_waiting_users().keys()),
        )
        if session is None:
            return None
        return tournament_id
