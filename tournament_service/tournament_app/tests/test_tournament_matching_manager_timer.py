import asyncio

from django.test import TestCase

from tournament_app.utils.tournament_matching_manager import (
    TournamentMatchingManager as Tmm,
)


class TournamentMatchingManagerTimerTest(TestCase):
    delay = 1

    async def __cancel_task_timer(self):
        """タスクとして実行される関数内でタイマーをキャンセル"""
        Tmm.cancel_task()

    async def test_cancel_task_timer(self):
        Tmm.set_task(self.delay, self.__cancel_task_timer)
        self.assertIsNotNone(Tmm.get_task())
        Tmm.cancel_task()
        await asyncio.sleep(0.1)
        self.assertIsNone(Tmm.get_task())

    async def test_cancel_task_timer_in_task(self):
        """
        タスクとして実行される関数内でタスクタイマーをキャンセルした場合
        """
        Tmm.set_task(self.delay, self.__cancel_task_timer)
        self.assertIsNotNone(Tmm.get_task())
        await asyncio.sleep(self.delay + 1)
        self.assertIsNone(Tmm.get_task())

    async def test_task_excution_time(self):
        """タスクが終了したらtask_execution_timeはNoneが返るか"""
        self.assertIsNone(Tmm.get_task_execution_time())
        Tmm.set_task(self.delay, self.__cancel_task_timer)
        self.assertIsNotNone(Tmm.get_task_execution_time())
        await asyncio.sleep(self.delay + 1)
        self.assertIsNone(Tmm.get_task_execution_time())
