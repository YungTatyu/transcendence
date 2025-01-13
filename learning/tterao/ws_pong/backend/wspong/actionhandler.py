from enum import Enum
from wspong.pingpong import PingPong


class ActionHandler:
    class ActionType(Enum):
        ACTION_PADDLE = "game.paddle_move"

    @staticmethod
    def handle(json, game):
        type = json.get("type")
        key = json.get("key")
        name = json.get("username")
        if type is None:
            return
        if type == ActionHandler.ActionType.ACTION_PADDLE:
            game.player_action(name, key)