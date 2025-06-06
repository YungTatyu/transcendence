import asyncio
from typing import Optional

from asgiref.sync import async_to_sync, sync_to_async
from channels.db import database_sync_to_async
from match_app.models import Match, MatchParticipant
from match_app.utils.match_finish_service import MatchFinishService
from match_app.utils.task_timer import TaskTimer


class TournamentMatchWaiter:
    __tournament_match_waiter_dict: dict[int, "TournamentMatchWaiter"] = {}
    # ユーザーの最初のアクセスから、強制的に試合を処理するまでの秒数
    LIMIT_WAIT_SEC = 180

    # 非同期排他制御用のlockオブジェクト
    __lock: Optional[asyncio.Lock] = None  # 初期化を遅延させるためNoneを設定

    def __init__(self, match_id: int):
        self.__match_id = match_id
        self.__task_timer = None
        self.__user_ids: list[int] = self.__fetch_user_ids(match_id)
        self.__connected_user_ids: list[int] = list()
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
        return self.__connected_user_ids

    @property
    def is_ready(self) -> bool:
        """試合参加者全員が試合待機部屋に入ったかどうか"""
        return len(self.__user_ids) == len(self.__connected_user_ids)

    def add_user(self, user_id):
        self.__connected_user_ids.append(user_id)

    def del_user(self, user_id):
        """
        ユーザーをTournamentMatchWaiterから削除、
        待機部屋に誰もいなくなった場合、インスタンスごと削除
        """
        if user_id in self.__connected_user_ids:
            self.__connected_user_ids.remove(user_id)
        # ユーザー退出後、誰も待機中でない場合、TournamentMatchWaiterごと削除
        if len(self.__connected_user_ids) == 0:
            TournamentMatchWaiter.delete(self.__match_id)

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
        if (待機部屋の人数 == 1) -> 不戦勝処理
        else -> 待機部屋にいる人のみでGameを開始させる
        """
        from match_app.consumers.tournament_match_consumer import (
            TournamentMatchConsumer,
        )

        match_id = self.match_id
        room_group_name = TournamentMatchConsumer.get_group_name(match_id)

        if len(self.__connected_user_ids) == 1:
            await self.handle_tournament_match_bye()
            await TournamentMatchConsumer.broadcast_start_match(
                room_group_name, None, self.connected_user_ids
            )
        else:
            await TournamentMatchConsumer.start_tournament_match(
                room_group_name, match_id
            )
        TournamentMatchWaiter.delete(self.match_id)

    async def handle_tournament_match_bye(self):
        """不戦勝となる場合、/matches/finishと同じ処理を実行"""
        results = []
        winner_user_id = int(self.__connected_user_ids[0])
        for user_id in self.__user_ids:
            score = 0 if user_id == winner_user_id else -1
            results.append({"userId": user_id, "score": score})
        await sync_to_async(
            MatchFinishService.update_match_data, thread_sensitive=False
        )(self.match_id, results)

        match = await sync_to_async(
            lambda: Match.objects.filter(match_id=self.match_id).first(),
            thread_sensitive=True,
        )()
        await sync_to_async(
            MatchFinishService.register_winner_in_parent_match, thread_sensitive=False
        )(match, results)
        err_message = await sync_to_async(
            MatchFinishService.send_match_result_to_tournament, thread_sensitive=False
        )(match)
        if err_message is not None:
            await sync_to_async(
                MatchFinishService.rollback_match_data, thread_sensitive=False
            )(self.match_id, match, results)

    def __fetch_user_ids(self, match_id: int) -> list[int]:
        participants = MatchParticipant.objects.filter(match_id=match_id)
        user_ids = [participant.user_id for participant in participants]
        return user_ids

    @staticmethod
    @database_sync_to_async
    def is_invalid_match_id(match_id: int, user_id) -> bool:
        """match_idが正しいかを確認"""
        #  既に登録済みで、開始前のmatch_idは正常
        tournament_match_waiter = TournamentMatchWaiter.search(match_id)
        if tournament_match_waiter:
            # 登録済みのuser_idの場合は拒否
            return user_id in tournament_match_waiter.connected_user_ids

        match = Match.objects.filter(match_id=match_id).first()

        if (
            not match  # 試合が存在しない
            or match.start_date is not None  # 試合が既に開始されている
            or match.finish_date is not None  # 試合が既に終了している
            or match.mode != "Tournament"  # 試合がTournamentの試合ではない
        ):
            return True

        curr_round = match.round
        # 初回のroundではない場合、一つ前のroundが終了しているかを確認
        if curr_round != 1:
            prev_round = curr_round - 1
            prev_match = Match.objects.filter(
                tournament_id=match.tournament_id, round=prev_round
            ).first()
            if prev_match.finish_date is None:
                return True

        # match_idに対応する試合にuser_idが参加者として登録されているか
        exist = MatchParticipant.objects.filter(
            match_id=match, user_id=user_id
        ).exists()
        return not exist

    @classmethod
    async def get_lock(cls) -> asyncio.Lock:
        if cls.__lock is None:
            cls.__lock = asyncio.Lock()  # イベントループ内で初期化
        return cls.__lock
