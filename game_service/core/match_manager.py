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

    class Keys(Enum):
        KEY_MATCH = "match"
        KEY_GAME_CONTROLLER = "game_contoroller"

    __matches = {}

    @classmethod
    def create_match(cls, match_id, players):
        """
        新しいMatchを作成
        """
        if match_id in MatchManager.__matches:
            raise ValueError(f"Match {match_id} already exists.")
        match = Match(match_id, players)
        MatchManager.__matches[match_id] = {
            MatchManager.Keys.KEY_MATCH.value: match,
            MatchManager.Keys.KEY_GAME_CONTROLLER.value: GameContoroller(match_id),
        }
        return MatchManager.__matches[match_id]

    @classmethod
    def get_match(cls, match_id):
        """
        指定されたMatchを取得
        """
        return MatchManager.__matches.get(match_id)

    @classmethod
    def remove_match(cls, match_id):
        """
        指定されたMatchを削除
        """
        if match_id in MatchManager.__matches:
            del MatchManager.__matches[match_id]

    @classmethod
    def delete_all_matches(cls):
        """すべてのマッチを削除する"""
        MatchManager.__matches.clear()
