from enum import Enum
from core.game_controller import GameContoroller


class Match:
    def __init__(self, match_id, players):
        self.match_id = match_id
        self.players = players


class MatchManager:
    """
    すべてのmatchを管理する
    """

    class MatchKeys(Enum):
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
            MatchManager.MatchKeys.KEY_GAME_CONTROLLER.value: GameContoroller(match_id),
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
