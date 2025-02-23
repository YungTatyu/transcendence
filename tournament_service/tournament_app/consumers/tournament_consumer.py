from channels.generic.websocket import AsyncWebsocketConsumer


class TournamentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # tournamentIdをURL から取得
        self.tournament_id = self.scope["url_route"]["kwargs"]["tournamentId"]
        # tournamentIdに紐づいたルーム
        self.room_group_name = f"tournament_{self.tournament_id}"

        # WebSocket グループに参加
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # TODO Tournamentの状況をSendする処理を追加

    async def disconnect(self, _):
        # WebSocket グループから退出
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, _):
        pass
