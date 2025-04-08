import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from tournament_app.consumers.tournament_state import TournamentState as State
from tournament_app.utils.tournament_session import TournamentSession


class TournamentConsumer(AsyncWebsocketConsumer):
    GROUP_NAME_FORMAT = "tournament_{}"

    @classmethod
    def get_group_name(cls, tournament_id: int):
        # 定数をフォーマットして使用
        return cls.GROUP_NAME_FORMAT.format(tournament_id)

    async def connect(self):
        if not self.scope.get("user_id"):
            await self.close()
            return

        self.user_id = int(self.scope.get("user_id"))

        # tournamentIdをURL から取得
        self.tournament_id = int(self.scope["url_route"]["kwargs"]["tournamentId"])
        # tournamentIdに紐づいたルーム
        self.room_group_name = TournamentConsumer.get_group_name(self.tournament_id)

        # TournamentSessionが存在しない場合、接続を拒否する
        tournament_session = TournamentSession.search(self.tournament_id)
        if tournament_session is None:
            await self.close(code=4400)
            return

        # 参加者ではないユーザーがトーナメントに参加しようとしている
        if self.user_id not in tournament_session.user_ids:
            await self.close(code=4400)
            return

        # WebSocket グループに参加
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        selected_protocol = self.scope.get("subprotocol")
        await self.accept(subprotocol=selected_protocol)

        # 接続してきたClientに試合状況をSend
        event = {
            "matches_data": tournament_session.matches_data,
            "current_round": tournament_session.current_round,
            "state": State.ONGOING,
        }
        await self.send_matches_data(event)

    async def disconnect(self, _):
        # WebSocket グループから退出
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def send_matches_data(self, event):
        """試合状況をクライアントに送信"""
        await self.send(
            text_data=json.dumps(
                {
                    "matches_data": event["matches_data"],
                    "current_round": event["current_round"],
                    "state": event["state"],
                }
            )
        )

    async def force_disconnect(self, _):
        await self.close(code=4200)

    @staticmethod
    async def broadcast_matches_info(state, tournament_id, matches_data, current_round):
        """Tournamentグループに対して試合状況をブロードキャスト"""
        channel_layer = get_channel_layer()
        group_name = TournamentConsumer.get_group_name(tournament_id)
        await channel_layer.group_send(
            group_name,
            {
                "type": "send_matches_data",
                "matches_data": matches_data,
                "current_round": current_round,
                "state": state,
            },
        )

    @staticmethod
    async def broadcast_force_disconnect(tournament_id):
        """TournamentグループのユーザーとのWebSocketを切断"""
        channel_layer = get_channel_layer()
        group_name = TournamentConsumer.get_group_name(tournament_id)
        await channel_layer.group_send(group_name, {"type": "force_disconnect"})
