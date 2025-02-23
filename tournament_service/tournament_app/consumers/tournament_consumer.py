import json
from channels.generic.websocket import AsyncWebsocketConsumer
from tournament_app.utils.tournament_session import TournamentSession


class TournamentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # tournamentIdをURL から取得
        self.tournament_id = self.scope["url_route"]["kwargs"]["tournamentId"]
        # tournamentIdに紐づいたルーム
        self.room_group_name = f"tournament_{self.tournament_id}"

        # TournamentSessionが存在しない場合、接続を拒否する
        tournament_session = TournamentSession.search(self.tournament_id)
        if tournament_session is None:
            await self.close(code=4400)
            return

        # WebSocket グループに参加
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # 接続してきたClientに試合状況をSend
        await self.send(
            self.channel_name,
            {
                "type": "send_matches_data",
                "matches_data": tournament_session.matches_data,
            },
        )

    async def disconnect(self, _):
        # WebSocket グループから退出
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def send_matches_data(self, event):
        """試合状況をクライアントに送信"""
        await self.send(text_data=json.dumps(event["matches_data"]))
