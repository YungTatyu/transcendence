import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from pingpong import PingPong


class GameManager:
    """
    インスタンスを作らない
    クラス変数ですべてのpingpongゲームを管理する
    """

    games = {}

    @classmethod
    def create_game(cls, match_id):
        if match_id in cls.games:
            return cls.games[match_id]
        cls.games[match_id] = PingPong()
        return cls.games[match_id]

    @classmethod
    def get_game(cls, match_id):
        """
        Return: Game or None
        """
        return cls.games.get(match_id)

    @classmethod
    def remove_game(cls, match_id):
        if match_id in cls.games:
            del cls.games[match_id]


class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.match_id = self.scope["url_route"]["kwargs"]["match_id"]
        self.username = self.scope["url_route"]["kwargs"]["username"]

        if self.match_id is None or self.username is None:
            return await self.disconnect_with_error_message(
                {"type": "error", "message": "missing match_id or username."}
            )

        self.game = GameManager.get_game(self.match_id)
        if self.game is None:
            self.game = GameManager.create_game(self.match_id)

        # TODO: user認証

        try:
            self.game.add_player(self.username)
        except RuntimeError as e:
            return await self.disconnect_with_error_message(
                {"type": "error", "message": f"{e}"}
            )

        # awiteはブロックするわけではない。処理を待つが待ってる間に他の処理を実行する
        await self.channel_layer.group_add(self.match_id, self.channel_name)
        await self.accept()

        if self.game.state == PingPong.GameState.READY_TO_START:
            pass

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.match_id, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(text_data_json)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "game.message"} | text_data_json,
        )

    # async_to_sync(self.channel_layer.group_send)の時にしてされたtypeがgame.messageのときにこの関数が呼ばれる
    async def game_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps(event))

    async def start_timer(self):
        """サーバーサイドのタイマー"""
        counter = 60
        while counter >= 0:
            # タイマーイベントを送信
            await self.channel_layer.group_send(
                self.room_group_name,
                {"type": "game.message", "message": "Timer Update", "timer": counter},
            )
            counter -= 1
            await asyncio.sleep(1)  # 1秒ごとに更新

    async def disconnect_with_error_message(self, json):
        await self.send(json.dumps(json))
        await self.close()
