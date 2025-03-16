import json
from channels.generic.websocket import AsyncWebsocketConsumer
from match_app.utils.tournament_match_waiter import TournamentMatchWaiter
from channels.layers import get_channel_layer


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

        if TournamentMatchWaiter.is_invalid_match_id(self.match_id, self.user_id):
            await self.close(code=4400)
            return

        # WebSocket グループに参加
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # TournamentMatchWaiterを取得し、登録されていない場合、登録する
        tournament_match_waiter = TournamentMatchWaiter.search(self.match_id)
        if tournament_match_waiter is None:
            tournament_match_waiter = TournamentMatchWaiter.register(self.match_id)

        tournament_match_waiter.add_user(self.user_id)

        # 参加者全員が揃った
        if tournament_match_waiter.is_ready:
            tournament_match_waiter.cancel_timer()
            await TournamentMatchConsumer.broadcast_start_match(
                self.match_id, tournament_match_waiter.connected_user_ids
            )
            TournamentMatchWaiter.delete(self.match_id)

    async def disconnect(self, _):
        pass

    @staticmethod
    async def broadcast_start_match(match_id: int, user_ids: list[int]):
        channel_layer = get_channel_layer()
        group_name = TournamentMatchConsumer.get_group_name(match_id)
        await channel_layer.group_send(
            group_name,
            {
                "type": "send_start_game",
                "match_id": str(match_id),
                "user_id_list": user_ids,
            },
        )

    async def send_start_game(self, event):
        await self.send(text_data=json.dumps({"match_id": event["match_id"]}))
