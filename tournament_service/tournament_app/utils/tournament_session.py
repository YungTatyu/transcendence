from typing import Optional


class TournamentSession:
    __tournament_session_dict: dict[int, "TournamentSession"] = {}

    def __init__(self, tournament_id: int, user_ids: list[int]):
        self.__tournament_id: int = tournament_id
        self.__current_round: int = 1
        self.__user_ids: list[int] = user_ids
        self.__create_matches_record(tournament_id, user_ids)

    @classmethod
    def register(
        cls, tournament_id: int, user_ids: list[int]
    ) -> Optional["TournamentSession"]:
        """既にセッションが存在する場合、何もしない"""
        if tournament_id in cls.__tournament_session_dict:
            return None
        tournament_session = TournamentSession(tournament_id, user_ids)
        cls.__tournament_session_dict[tournament_id] = tournament_session
        return tournament_session

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

    # TODO 実際にmatchesAPIを叩き、レコードを作成する処理
    def __create_matches_record(self, tournament_id: int, user_ids: list[int]):
        """matchesサーバのAPIを叩き、レコードを作成する処理"""
        pass
