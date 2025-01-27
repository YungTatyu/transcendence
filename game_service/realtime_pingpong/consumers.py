from enum import Enum
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer

from core.match_manager import MatchManager
import jwt

from core.pingpong import PingPong


class AuthHandler:
    """
    TODO: wsでjwt認証をどうするか？
    headerで渡すには、フロントのライブラリを使用しなければいけないみたい
    """

    @staticmethod
    def search_jwt(headers):
        for header in headers:
            if header[0] == b"cookie":
                cookies = header[1].decode()
                # JWTが含まれるCookie名を指定して取り出す
                for cookie in cookies.split(";"):
                    if "jwt_token=" in cookie:
                        return cookie.split("jwt_token=")[1]
        return None

    def verify_jwt(self, token):
        # JWTの検証ロジック
        try:
            decoded = jwt.decode(token, "your-secret-key", algorithms=["HS256"])
            return True
        except jwt.ExpiredSignatureError:
            return False
        except jwt.InvalidTokenError:
            return False

    def get_user_id_from_jwt(self, token):
        # JWTからユーザーIDを取得
        decoded = jwt.decode(token, "your-secret-key", algorithms=["HS256"])
        return decoded.get("sub")  # 例: "sub"にユーザーIDを保存している場合


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
        if user_id not in match.users:
            return (False, 1008)

        # TODO: user認証

        game_contoroller = match_dict[MatchManager.KEY_GAME_CONTROLLER]
        game = game_contoroller.game
        try:
            game.add_player(user_id)
        except RuntimeError as e:
            # 1007(矛盾するデータ)
            return (False, 1007)
        return (True,)

    @staticmethod
    def handle_player_action(json, game):
        type = json.get("type")
        key = json.get("key")
        name = json.get("userid")
        if type is None:
            return
        if type == ActionHandler.ACTION_PADDLE:
            game.player_action(name, key):


class GameConsumer(AsyncWebsocketConsumer):
    """
    wsの通信, I/O処理を責務とする
    """

    class MessageType(Enum):
        MSG_UPDATE = "game update"
        MSG_ERROR = "error"
        MSG_GAME_OVER = "game over"

    async def connect(self):
        self.match_id = self.scope["url_route"]["kwargs"]["match_id"]
        # TODO
        # 本来はuriに含めないが認証の処理に影響するため、一旦仕様を変える
        self.user_id = self.scope["url_route"]["kwargs"]["userid"]

        re, status_code = ActionHandler.handle_new_connection(
            self.match_id, self.user_id
        )
        if not re:
            await self.close(code=status_code)
            return

        await self.channel_layer.group_add(self.match_id, self.channel_name)
        await self.accept()

        if game.state == PingPong.GameState.READY_TO_START:
            game_contoroller.start_game(self.match_id)

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.match_id, self.channel_name)
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
    async def group_send(event, match_id):
        channel_layer = get_channel_layer()
        event["type"] = "game.message"
        await channel_layer.group_send(match_id, event)
