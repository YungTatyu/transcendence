class TournamentSession:
    __tournament_session_dict = dict()

    def __init__(self, tournament_id: int, user_ids: list[int]):
        self.__tournament_id: int = tournament_id
        self.__now_round: int = 1
        self.__user_ids: list[int] = user_ids
        self.__create_matches_record(tournament_id, user_ids)

    @classmethod
    def register_tournament_session(cls, tournament_id: int, user_ids: list[int]):
        tournament_session = TournamentSession(tournament_id, user_ids)
        cls.__tournament_session_dict[tournament_id] = tournament_session
        return tournament_session

    @classmethod
    def search_tournament_session(cls, tournament_id: int):
        return cls.__tournament_session_dict.get(tournament_id, None)

    @classmethod
    def del_tournament_session(cls, tournament_id: int) -> bool:
        if cls.search_tournament_session(tournament_id):
            del cls.__tournament_session_dict[tournament_id]
            return True
        return False

    @property
    def now_round(self) -> int:
        return self.__now_round

    def next_round(self) -> int:
        self.__now_round += 1
        return self.__now_round

    # TODO 実際にmatchesAPIを叩き、レコードを作成する処理
    def __create_matches_record(self, tournament_id: int, user_ids: list[int]):
        """matchesサーバのAPIを叩き、レコードを作成する処理"""
        pass
