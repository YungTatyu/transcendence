import json
from typing import Optional

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from django.conf import settings
from django.utils.timezone import now
from match_app.client.game_client import GameClient
from match_app.models import Match
from match_app.utils.tournament_match_waiter import TournamentMatchWaiter


class TournamentMatchConsumer(AsyncWebsocketConsumer):
    GROUP_NAME_FORMAT = "match_{}"

    @classmethod
    def get_group_name(cls, match_id: int):
        # 定数をフォーマットして使用
        return cls.GROUP_NAME_FORMAT.format(match_id)

    async def connect(self):
        self.user_id = self.scope.get("user_id")
        if not self.user_id:
            await self.close()
            return

        self.match_id = int(self.scope["url_route"]["kwargs"]["matchId"])
        self.room_group_name = TournamentMatchConsumer.get_group_name(self.match_id)

        if await TournamentMatchWaiter.is_invalid_match_id(self.match_id, self.user_id):
            await self.close(code=4400)
            return

        # WebSocket グループに参加
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        selected_protocol = self.scope.get("subprotocol")
        await self.accept(subprotocol=selected_protocol)

        # Lockを用いて1人ずつ処理(パフォーマンスを犠牲に整合性を保つ)
        lock = await TournamentMatchWaiter.get_lock()
        async with lock:
            # TournamentMatchWaiterを取得し、登録されていない場合、登録する
            tournament_match_waiter = TournamentMatchWaiter.search(self.match_id)
            if tournament_match_waiter is None:
                tournament_match_waiter = await database_sync_to_async(
                    TournamentMatchWaiter.register
                )(self.match_id)

            tournament_match_waiter.add_user(self.user_id)

            # 参加者全員が揃った
            if tournament_match_waiter.is_ready:
                tournament_match_waiter.cancel_timer()
                await self.start_tournament_match(self.room_group_name, self.match_id)
                TournamentMatchWaiter.delete(self.match_id)

    async def disconnect(self, _):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        tournament_match_waiter = TournamentMatchWaiter.search(self.match_id)
        if tournament_match_waiter is not None:
            tournament_match_waiter.del_user(self.user_id)

    @staticmethod
    async def start_tournament_match(group_name, match_id):
        """
        GameAPIを叩き、リソースを作成
        試合開始時刻を更新
        試合開始情報をClientにSend
        """
        tournament_match_waiter = TournamentMatchWaiter.search(match_id)
        user_ids = tournament_match_waiter.connected_user_ids

        # GameAPIを叩き、ゲーム開始の準備を行う
        client = GameClient(settings.GAME_API_BASE_URL)
        res_data = await client.fetch_games(
            match_id, tournament_match_waiter.connected_user_ids
        )
        if res_data.get("error", None) is not None:
            # INFO 内部エラーが起きたときはユーザーに`match_id: "None"`を返す
            match_id = None
        else:
            # start_dateを現在時刻で更新する
            await database_sync_to_async(
                lambda: Match.objects.filter(match_id=match_id).update(start_date=now())
            )()

        await TournamentMatchConsumer.broadcast_start_match(
            group_name, match_id, user_ids
        )

    @staticmethod
    async def broadcast_start_match(
        group_name: str, match_id: Optional[int], user_ids: list[int]
    ):
        channel_layer = get_channel_layer()
        await channel_layer.group_send(
            group_name,
            {
                "type": "send_start_game",
                "match_id": str(match_id),
                "user_id_list": user_ids,
            },
        )

    async def send_start_game(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "match_id": event["match_id"],
                    "user_id_list": event["user_id_list"],
                }
            )
        )
