import json
from enum import Enum

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from core.match_manager import MatchManager
from core.pingpong import PingPong
from realtime_pingpong import game_controller

# class AuthHandler:
#     """
#     TODO: wsでjwt認証をどうするか？
#     headerで渡すには、フロントのライブラリを使用しなければいけないみたい
#     """
#
#     @staticmethod
#     def search_jwt(headers):
#         for header in headers:
#             if header[0] == b"cookie":
#                 cookies = header[1].decode()
#                 # JWTが含まれるCookie名を指定して取り出す
#                 for cookie in cookies.split(";"):
#                     if "jwt_token=" in cookie:
#                         return cookie.split("jwt_token=")[1]
#         return None
#
#     def verify_jwt(self, token):
#         # JWTの検証ロジック
#         try:
#             jwt.decode(token, "your-secret-key", algorithms=["HS256"])
#             return True
#         except jwt.ExpiredSignatureError:
#             return False
#         except jwt.InvalidTokenError:
#             return False
#
#     def get_user_id_from_jwt(self, token):
#         # JWTからユーザーIDを取得
#         decoded = jwt.decode(token, "your-secret-key", algorithms=["HS256"])
#         return decoded.get("sub")  # 例: "sub"にユーザーIDを保存している場合
#


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
            # acceptしていないので、エラーメッセージは送信不可
            # 1008 (Policy Violation)
            return (False, 1008)

        match_dict = MatchManager.get_match(match_id)
        if match_dict is None:
            # 1003 (Unsupported Data)
            return (False, 1003)

        match = match_dict[MatchManager.KEY_MATCH]
        if user_id not in match.players:
            return (False, 1008)

        # TODO: user認証

        game_contoroller = match_dict[MatchManager.KEY_GAME_CONTROLLER]
        game = game_contoroller.game
        try:
            game.add_player(user_id)
        except RuntimeError:
            # 1007(矛盾するデータ)
            return (False, 1007)
        return (True, 200)

    @staticmethod
    def handle_player_action(json, game):
        type = json.get("type")
        key = json.get("key")
        if type is None:
            return
        try:
            id = int(json.get("userid"))
        except ValueError:
            return
        if type == ActionHandler.ACTION_PADDLE:
            game.player_action(id, key)

    @staticmethod
    def handle_game_connection(match_id, player_id):
        match_dict = MatchManager.get_match(match_id)
        game_contoroller = match_dict[MatchManager.KEY_GAME_CONTROLLER]
        game = game_contoroller.game
        if game.state == PingPong.GameState.READY_TO_START:
            return game_contoroller.start_game(str(match_id))
        elif game.state == PingPong.GameState.IN_PROGRESS:  # game再接続
            return game_controller.reconnect_event(str(match_id), player_id)


class GameConsumer(AsyncWebsocketConsumer):
    """
    wsの通信, I/O処理を責務とする
    """

    class MessageType(Enum):
        MSG_UPDATE = "update"
        MSG_ERROR = "error"
        MSG_TIMER = "timer"
        MSG_GAME_OVER = "gameover"

    async def connect(self):
        # group nameはstrである必要がある
        self.group_name = self.scope["url_route"]["kwargs"]["matchId"]
        self.match_id = int(self.group_name)
        # TODO
        # 本来はuriに含めないが認証の処理に影響するため、一旦仕様を変える
        self.user_id = int(self.scope["url_route"]["kwargs"]["userId"])

        re, status_code = ActionHandler.handle_new_connection(
            self.match_id, self.user_id
        )
        if not re:
            await self.close(code=status_code)
            return

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        ActionHandler.handle_game_connection(self.match_id, self.user_id)

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        MatchManager.remove_match(self.match_id)
        await self.close(close_code)

    async def receive(self, text_data):
        match_dict = MatchManager.get_match(self.match_id)
        game = match_dict[MatchManager.KEY_GAME_CONTROLLER].game
        text_data_json = json.loads(text_data)
        ActionHandler.handle_player_action(text_data_json, game)

    # async_to_sync(self.channel_layer.group_send)の時にしてされたtypeがgame.messageのときにこの関数が呼ばれる
    async def game_message(self, event):
        await self.send(text_data=json.dumps(event))

    @staticmethod
    async def group_send(event, group_name):
        channel_layer = get_channel_layer()
        event["type"] = "game.message"
        await channel_layer.group_send(group_name, event)
