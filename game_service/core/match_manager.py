from realtime_pingpong.game_controller import GameController


class Match:
    def __init__(self, match_id, players):
        self.match_id = match_id
        self.players = players


class MatchManager:
    """
    すべてのmatchを管理する
    """

    KEY_MATCH = "match"
    KEY_GAME_CONTROLLER = "game_contoroller"

    __matches: dict[int, dict[str, Match | GameController]] = {}

    @classmethod
    def create_match(cls, match_id, players):
        """
        新しいmatch_dictを作成
        """
        if match_id in MatchManager.__matches:
            raise ValueError(f"Match {match_id} already exists.")
        match = Match(match_id, players)
        MatchManager.__matches[match_id] = {
            MatchManager.KEY_MATCH: match,
            MatchManager.KEY_GAME_CONTROLLER: GameController(),
        }
        return MatchManager.__matches[match_id]

    @classmethod
    def get_match(cls, match_id):
        """
        指定されたmatch_dictを取得

        Returns:
            dict[str, Match | GameController] | None:
                指定されたmatch_idに対応する辞書を返す
                - "match": Match 型のオブジェクト
                - "game_controller": GameController 型のオブジェクト
                match_id が見つからない場合は None を返す
        """
        return MatchManager.__matches.get(match_id)

    @classmethod
    def remove_match(cls, match_id):
        """
        指定されたmatch_dictを削除
        """
        if match_id in MatchManager.__matches:
            del MatchManager.__matches[match_id]

    @classmethod
    def delete_all_matches(cls):
        """すべてのマッチを削除する"""
        MatchManager.__matches.clear()
