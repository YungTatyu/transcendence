from typing import Optional
from match_app.utils.task_timer import TaskTimer


class TournamentMatchWaiter:
    __tournament_match_waiter_dict: dict[int, "TournamentMatchWaiter"]
    # ユーザーの最初のアクセスから、強制的に試合を処理するまでの秒数
    LIMIT_WAIT_SEC = 5

    def __init__(self, match_id: int):
        self.__match_id = match_id
        self.__task_timer = None
        # TODO match_idを用いてDB内からuser_idsを取得する処理
        # TODO 強制処理タイマーセット

    @classmethod
    def register(cls, match_id: int) -> Optional["TournamentMatchWaiter"]:
        if match_id in cls.__tournament_match_waiter_dict:
            return None
        tournament_match = TournamentMatchWaiter(match_id)
        cls.__tournament_match_waiter_dict[match_id] = tournament_match
        return tournament_match

    @classmethod
    def search(cls, match_id: int) -> Optional["TournamentMatchWaiter"]:
        return cls.__tournament_match_waiter_dict.get(match_id, None)

    @classmethod
    def delete(cls, match_id: int) -> bool:
        if cls.search(match_id):
            del cls.__tournament_match_waiter_dict[match_id]
            return True
        return False

    @classmethod
    def clear(cls):
        cls.__tournament_match_waiter_dict.clear()

    @property
    def match_id(self) -> int:
        return self.__match_id

    async def set_wait_timer(self):
        """
        トーナメント試合の参加者が永遠に揃わない状況を防ぐ
        """
        self.__task_timer = TaskTimer(
            self.LIMIT_WAIT_SEC, self.handle_fallback_tournament_match
        )

    async def handle_fallback_tournament_match(self):
        pass
