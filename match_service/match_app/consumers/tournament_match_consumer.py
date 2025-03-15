from channels.generic.websocket import AsyncWebsocketConsumer


class TournamentMatchConsumer(AsyncWebsocketConsumer):
    GROUP_NAME_FORMAT = "match_{}"

    @classmethod
    def get_group_name(cls, match_id: int):
        # 定数をフォーマットして使用
        return cls.GROUP_NAME_FORMAT.format(match_id)

    async def connect(self):
        self.match_id = int(self.scope["url_route"]["kwargs"]["matchId"])
        self.room_group_name = TournamentMatchConsumer.get_group_name(self.match_id)

        # TODO participants = get_match_data()
        # if not self.user_id in participants:
        #     await self.close(code=4400)
        #     return

        # WebSocket グループに参加
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        pass

    async def disconnect(self, _):
        pass
