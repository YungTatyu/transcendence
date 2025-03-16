from typing import Optional
from match_app.utils.task_timer import TaskTimer
from asgiref.sync import async_to_sync
from match_app.models import Match, MatchParticipant
from channels.db import database_sync_to_async


class TournamentMatchWaiter:
    __tournament_match_waiter_dict: dict[int, "TournamentMatchWaiter"] = {}
    # ユーザーの最初のアクセスから、強制的に試合を処理するまでの秒数
    LIMIT_WAIT_SEC = 5

    def __init__(self, match_id: int):
        self.__match_id = match_id
        self.__task_timer = None
        self.__user_ids: set[int] = self.__fetch_user_ids(match_id)
        self.__connected_user_ids: set[int] = set()
        async_to_sync(self.set_wait_timer, force_new_loop=False)()

    @classmethod
    def register(cls, match_id: int) -> "TournamentMatchWaiter":
        tournament_match = TournamentMatchWaiter(match_id)
        cls.__tournament_match_waiter_dict[match_id] = tournament_match
        return tournament_match

    @classmethod
    def search(cls, match_id: int) -> Optional["TournamentMatchWaiter"]:
        return cls.__tournament_match_waiter_dict.get(match_id, None)

    @classmethod
    def delete(cls, match_id: int) -> bool:
        if cls.search(match_id):
            tournament_match_waiter = cls.__tournament_match_waiter_dict[match_id]
            tournament_match_waiter.cancel_timer()
            del cls.__tournament_match_waiter_dict[match_id]
            return True
        return False

    @classmethod
    def clear(cls):
        for tournament_match in cls.__tournament_match_waiter_dict.values():
            tournament_match.cancel_timer()
        cls.__tournament_match_waiter_dict.clear()

    @property
    def match_id(self) -> int:
        return self.__match_id

    @property
    def connected_user_ids(self) -> list[int]:
        return list(self.__connected_user_ids)

    @property
    def is_ready(self) -> bool:
        return len(self.__user_ids) == len(self.__connected_user_ids)

    def add_user(self, user_id):
        self.__connected_user_ids.add(user_id)

    def del_user(self, user_id):
        self.__connected_user_ids.remove(user_id)

    def cancel_timer(self):
        if self.__task_timer is not None:
            self.__task_timer.cancel()

    async def set_wait_timer(self):
        """
        トーナメント試合の参加者が永遠に揃わない状況を防ぐ
        """
        self.__task_timer = TaskTimer(
            self.LIMIT_WAIT_SEC, self.handle_fallback_tournament_match
        )

    async def handle_fallback_tournament_match(self):
        """
        トーナメント試合に参加者全員が揃わない場合に強制的行われる処理
        """
        from match_app.consumers.tournament_match_consumer import (
            TournamentMatchConsumer,
        )

        if len(self.__connected_user_ids) == 1:
            # TODO DBにレコードを挿入し、/tournaments/finish-matchエンドポイントを叩く
            return

        await TournamentMatchConsumer.broadcast_start_match(
            self.match_id, self.connected_user_ids
        )
        # 現在いるユーザーのみにSendする
        TournamentMatchWaiter.delete(self.match_id)
        self.cancel_timer()

    def __fetch_user_ids(self, match_id: int) -> set[int]:
        participants = MatchParticipant.objects.filter(match_id=match_id)
        user_ids = {participant.user_id for participant in participants}
        return user_ids

    @staticmethod
    @database_sync_to_async
    def is_invalid_match_id(match_id: int, user_id) -> bool:
        """match_idが正しいかを確認"""
        #  既に登録済みで、開始前のmatch_idは正常
        if TournamentMatchWaiter.search(match_id):
            return False

        match = Match.objects.filter(match_id=match_id).first()

        if (
            not match  # 試合が存在しない
            or match.finish_date is not None  # 試合が既に終了している
            or match.mode != "Tournament"  # 試合がTournamentの試合ではない
        ):
            return True

        curr_round = match.round
        # 初回のroundではない場合、一つ前のroundが終了しているかを確認
        if curr_round != 1:
            prev_round = curr_round - 1
            prev_match = Match.objects.filter(match_id=match_id, round=prev_round)
            if prev_match.finish_date is None:
                return True

        # match_idに対応する試合にuser_idが参加者として登録されているか
        exist = MatchParticipant.objects.filter(
            match_id=match, user_id=user_id
        ).exists()
        return not exist
