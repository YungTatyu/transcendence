import json
from dataclasses import dataclass

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from core.match_manager import MatchManager
from core.pingpong import PingPong


class ActionHandler:
    """
    ws connectionのhandler
    """

    ACTION_PADDLE = "game.paddle_move"

    @staticmethod
    def handle_new_connection(match_id, user_id):
        """
        returns: True|False, status code
        """
        if match_id is None or user_id is None:
            # 1008 (Policy Violation)
            return (False, 1008)

        match_dict = MatchManager.get_match(match_id)
        if match_dict is None:
            # 1003 (Unsupported Data)
            return (False, 1003)

        match = match_dict[MatchManager.KEY_MATCH]
        if user_id not in match.players:
            return (False, 1008)

        game_contoroller = match_dict[MatchManager.KEY_GAME_CONTROLLER]
        if game_contoroller.player_manager.is_active(user_id):
            return (False, 1008)
        game = game_contoroller.game
        game.add_player(user_id, match.players.index(user_id))
        return (True, 200)

    @staticmethod
    def handle_player_action(json, game, user_id):
        type = json.get("type")
        key = json.get("key")
        if not all([type, key]):
            return
        if type == ActionHandler.ACTION_PADDLE:
            game.player_action(user_id, key)

    @staticmethod
    async def handle_game_connection(match_id, player_id):
        match_dict = MatchManager.get_match(match_id)
        game_controller = match_dict[MatchManager.KEY_GAME_CONTROLLER]
        game = game_controller.game
        if game.state == PingPong.GameState.READY_TO_START:
            return game_controller.start_game(str(match_id))
        elif game.state == PingPong.GameState.IN_PROGRESS:  # game再接続
            return await game_controller.reconnect_event(str(match_id), player_id)

    @staticmethod
    def handle_disconnection(match_id, player_id):
        match_dict = MatchManager.get_match(match_id)
        # 既にmatchが削除されている
        if match_dict is None:
            return
        game_controller = match_dict[MatchManager.KEY_GAME_CONTROLLER]
        return game_controller.disconnect_event(player_id)

    @staticmethod
    def handle_game_end(match_id):
        MatchManager.remove_match(match_id)


class GameConsumer(AsyncWebsocketConsumer):
    """
    wsの通信, I/O処理を責務とする
    """

    @dataclass(frozen=True)
    class MessageType:
        MSG_UPDATE = "update"
        MSG_ERROR = "error"
        MSG_TIMER = "timer"
        MSG_GAME_OVER = "gameover"

    async def connect(self):
        # group nameはstrである必要がある
        self.group_name = self.scope["url_route"]["kwargs"]["matchId"]
        self.match_id = int(self.group_name)
        if self.scope.get("user_id") is None:
            await self.close()
            return
        self.user_id = int(self.scope.get("user_id"))

        re, status_code = ActionHandler.handle_new_connection(
            self.match_id, self.user_id
        )
        if not re:
            # acceptしていないので、エラーメッセージは送信不可
            await self.close(code=status_code)
            return

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        selected_protocol = self.scope.get("subprotocol")
        await self.accept(subprotocol=selected_protocol)
        await ActionHandler.handle_game_connection(self.match_id, self.user_id)

    async def disconnect(self, close_code=1000):
        """
        defaultは正常終了(1000)
        """
        ActionHandler.handle_disconnection(self.match_id, self.user_id)
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        await self.close(close_code)

    async def receive(self, text_data):
        match_dict = MatchManager.get_match(self.match_id)
        # 既にmatchが削除されている
        if match_dict is None:
            return
        game = match_dict[MatchManager.KEY_GAME_CONTROLLER].game
        text_data_json = json.loads(text_data)
        ActionHandler.handle_player_action(text_data_json, game, self.user_id)

    # channel_layer.group_sendのtypeがgame.messageのときにこの関数が呼ばれる
    async def game_message(self, event):
        await self.send(text_data=json.dumps(event))

    @staticmethod
    async def group_send(event, group_name):
        channel_layer = get_channel_layer()
        event["type"] = "game.message"
        await channel_layer.group_send(group_name, event)

    async def game_finish_message(self, event):
        await self.send(text_data=json.dumps(event))
        await self.disconnect()

    @staticmethod
    async def finish_game(event, group_name):
        channel_layer = get_channel_layer()
        event["type"] = "game.finish.message"
        await channel_layer.group_send(group_name, event)
        ActionHandler.handle_game_end(int(group_name))
