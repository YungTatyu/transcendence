from typing import Optional

from tournament_app.utils.match_client import MatchClient
from tournament_app.utils.tournament_tree import TournamentTree


class TournamentSession:
    __tournament_session_dict: dict[int, "TournamentSession"] = {}

    def __init__(self, tournament_id: int, user_ids: list[int]):
        """
        [INFO] match作成処理失敗の場合、例外が発生、インスタンスは作成されない
        """
        self.__tournament_id: int = tournament_id
        self.__current_round: int = 1
        self.__user_ids: list[int] = user_ids
        self.__create_match_records(tournament_id, user_ids)

    @classmethod
    def register(
        cls, tournament_id: int, user_ids: list[int]
    ) -> Optional["TournamentSession"]:
        """
        (既にセッションが存在 OR match作成処理失敗) => return None
        [INFO] match作成処理失敗の場合、registerされない
        """
        if tournament_id in cls.__tournament_session_dict:
            return None
        try:
            tournament_session = TournamentSession(tournament_id, user_ids)
            cls.__tournament_session_dict[tournament_id] = tournament_session
            return tournament_session
        except Exception:
            return None

    @classmethod
    def search(cls, tournament_id: int) -> Optional["TournamentSession"]:
        return cls.__tournament_session_dict.get(tournament_id, None)

    @classmethod
    def delete(cls, tournament_id: int) -> bool:
        if cls.search(tournament_id):
            del cls.__tournament_session_dict[tournament_id]
            return True
        return False

    @classmethod
    def clear(cls):
        cls.__tournament_session_dict.clear()

    @property
    def tournament_id(self) -> int:
        return self.__tournament_id

    @property
    def user_ids(self) -> list[int]:
        return self.__user_ids

    @property
    def current_round(self) -> int:
        return self.__current_round

    def next_round(self) -> int:
        self.__current_round += 1
        return self.__current_round

    def __create_match_records(self, tournament_id: int, user_ids: list[int]):
        """
        matchesサーバのAPIを叩き、レコードを作成する処理
        [WARN] matchAPIを叩く処理でエラーが発生した場合、例外が発生
        """
        tree = TournamentTree(user_ids)
        client = MatchClient("http://localhost:8002")

        for node in TournamentTree.bfs_iterator(tree.root):
            parent = node.parent_node
            parent_match_id = None if parent is None else parent.match_id
            response = client.create_tournament_match_record(
                node.value_list, tournament_id, parent_match_id, node.round
            )

            if response.status_code != 200:
                raise Exception
            node.match_id = int(response.text)
