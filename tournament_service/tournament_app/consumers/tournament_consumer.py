import json

from channels.generic.websocket import AsyncWebsocketConsumer
from tournament_app.utils.tournament_session import TournamentSession
from tournament_app.consumers.tournament_state import TournamentState as State


class TournamentConsumer(AsyncWebsocketConsumer):
    GROUP_NAME_FORMAT = "tournament_{}"

    @classmethod
    def get_group_name(cls, tournament_id: int):
        # 定数をフォーマットして使用
        return cls.GROUP_NAME_FORMAT.format(tournament_id)

    async def connect(self):
        # tournamentIdをURL から取得
        self.tournament_id = self.scope["url_route"]["kwargs"]["tournamentId"]
        # tournamentIdに紐づいたルーム
        self.room_group_name = TournamentConsumer.get_group_name(self.tournament_id)

        # TournamentSessionが存在しない場合、接続を拒否する
        tournament_session = TournamentSession.search(int(self.tournament_id))
        if tournament_session is None:
            await self.close(code=4400)
            return

        # WebSocket グループに参加
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

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
            text_data=json.dumps({
                "matches_data": event["matches_data"],
                "current_round": event["current_round"],
                "state": event["state"],
            })
        )

    async def force_disconnect(self, _):
        """トーナメントが終了した際にサーバからWebSocketを切断するための関数"""
        await self.close(code=4200)
