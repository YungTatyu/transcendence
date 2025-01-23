import asyncio

from django.test import TestCase

from tournament_app.utils.tournament_matching_manager import (
    TournamentMatchingManager as TMM,
)


class TournamentMatchingManagerTimerTest(TestCase):
    delay = 1

    async def __cancel_task_timer(self):
        """タスクとして実行される関数内でタイマーをキャンセル"""
        TMM.cancel_task()

    async def test_cancel_task_timer(self):
        TMM.set_task(self.delay, self.__cancel_task_timer)
        self.assertIsNotNone(TMM.get_task())
        TMM.cancel_task()
        await asyncio.sleep(0.1)
        self.assertIsNone(TMM.get_task())

    async def test_cancel_task_timer_in_task(self):
        """
        タスクとして実行される関数内でタスクタイマーをキャンセルした場合
        """
        TMM.set_task(self.delay, self.__cancel_task_timer)
        self.assertIsNotNone(TMM.get_task())
        await asyncio.sleep(self.delay + 1)
        self.assertIsNone(TMM.get_task())

    async def test_task_excution_time(self):
        """タスクが終了したらtask_execution_timeはNoneが返るか"""
        self.assertIsNone(TMM.get_task_execution_time())
        TMM.set_task(self.delay, self.__cancel_task_timer)
        self.assertIsNotNone(TMM.get_task_execution_time())
        await asyncio.sleep(self.delay + 1)
        self.assertIsNone(TMM.get_task_execution_time())
