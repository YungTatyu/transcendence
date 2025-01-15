import enum
import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from wspong.actionhandler import ActionHandler
from wspong.pingpong import PingPong


class Match:
    def __init__(self, match_id, players):
        self.match_id = match_id
        self.players = players


class MatchManager:
    class MatchKeys(enum.Enum):
        KEY_MATCH = "match"
        KEY_GAME_CONTROLLER = "game_contoroller"

    __matches = {}

    @staticmethod
    def create_match(match_id, players):
        """
        新しいMatchを作成
        """
        if match_id in MatchManager.__matches:
            raise ValueError(f"Match {match_id} already exists.")
        match = Match(match_id, players)
        MatchManager.__matches[match_id] = {
            MatchManager.MatchKeys.KEY_MATCH.value: match,
            MatchManager.MatchKeys.KEY_GAME_CONTROLLER.value: GameContoroller(),
        }
        return MatchManager.__matches[match_id]

    @staticmethod
    def get_match(match_id):
        """
        指定されたMatchを取得
        """
        return MatchManager.__matches.get(match_id)

    @staticmethod
    def remove_match(match_id):
        """
        指定されたMatchを削除
        """
        if match_id in MatchManager.__matches:
            del MatchManager.__matches[match_id]


class GameContoroller:
    """
    game進行を管理する
    """

    def __init__(self):
        self.game = PingPong()
        self.__task = None

    def start_game(self, match_id):
        if self.__task is not None:
            raise RuntimeError("task alredy exists.")
        self.__task = asyncio.create_task(self.game_loop(match_id))

    def stop_game(self):
        if self.task is not None:
            self.task.cancel()
            self.task = None

    async def game_loop(self, match_id):
        try:
            while self.game.state != PingPong.GameState.GAME_OVER:
                self.game.update()
                await GameConsumer.group_send(
                    {
                        "message": GameConsumer.MessageType.MSG_UPDATE.value,
                        "data": {
                            "state": self.game.get_state(),
                        },
                    },
                    match_id,
                )
                await asyncio.sleep(1 / 60)  # 60FPS (約16.67ミリ秒間隔)
        except asyncio.CancelledError:
            print("Game loop was cancelled.")


class GameConsumer(AsyncWebsocketConsumer):
    """
    wsの通信, I/O処理を責務とする
    """

    class MessageType(enum.Enum):
        MSG_UPDATE = "game update"
        MSG_ERROR = "error"
        MSG_GAME_OVER = "game over"

    async def connect(self):
        self.match_id = self.scope["url_route"]["kwargs"]["match_id"]
        self.username = self.scope["url_route"]["kwargs"]["username"]

        if self.match_id is None or self.username is None:
            return await self.disconnect_with_error_message(
                {
                    "type": self.MessageType.MSG_ERROR.value,
                    "message": "missing match_id or username.",
                }
            )

        match_dict = MatchManager.get_match(self.match_id)
        if match_dict is None:
            match_dict = MatchManager.create_match(self.match_id, ["aa", "bb"])

        # TODO: user認証

        game_contoroller = match_dict[MatchManager.MatchKeys.KEY_GAME_CONTROLLER.value]
        game = game_contoroller.game

        try:
            game.add_player(self.username)
        except RuntimeError as e:
            return await self.disconnect_with_error_message(
                {"type": self.MessageType.MSG_ERROR.value, "message": f"{e}"}
            )

        # awiteはブロックするわけではない。処理を待つが待ってる間に他の処理を実行する
        await self.channel_layer.group_add(self.match_id, self.channel_name)
        await self.accept()

        if game.state == PingPong.GameState.READY_TO_START:
            game_contoroller.start_game(self.match_id)

    async def disconnect(self, close_code):
        # Leave room group
        print(f"leaving channel {self.channel_name} and group {self.match_id}")
        await self.channel_layer.group_discard(self.match_id, self.channel_name)
        MatchManager.remove_match(self.match_id)

    async def receive(self, text_data):
        match_dict = MatchManager.get_match(self.match_id)
        game = match_dict[MatchManager.MatchKeys.KEY_GAME_CONTROLLER.value].game
        text_data_json = json.loads(text_data)
        ActionHandler.handle_player_action(text_data_json, game)

    # async_to_sync(self.channel_layer.group_send)の時にしてされたtypeがgame.messageのときにこの関数が呼ばれる
    async def game_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps(event))

    @staticmethod
    async def group_send(event, match_id):
        print("group_send called")
        print("data", event)
        channel_layer = get_channel_layer()
        event["type"] = "game.message"
        await channel_layer.group_send(match_id, event)

    async def game_loop(self):
        print("game loop start")
        while self.game.state != PingPong.GameState.GAME_OVER:
            self.game.update()
            print("group sending state", self.game.get_state())
            await self.channel_layer.group_send(
                self.match_id,
                {
                    "type": "game.message",
                    "message": self.MessageType.MSG_UPDATE.value,
                    "data": {
                        "state": self.game.get_state(),
                    },
                },
            )
            print("sent state")
            await asyncio.sleep(1 / 60)  # 60FPS

        print("game loop end")

    async def disconnect_with_error_message(self, json):
        await self.send(json.dumps(json))
        await self.close()
