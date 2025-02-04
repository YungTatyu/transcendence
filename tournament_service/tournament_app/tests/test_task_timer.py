import asyncio
import time

from django.test import TestCase

from tournament_app.utils.task_timer import TaskTimer


class TaskTimerTest(TestCase):
    delay = 1

    async def __do_nothing(self):
        pass

    async def __return_value(self, value: int) -> int:
        return value

    async def test_execute_task(self):
        """タスクが終了するか"""
        task_timer = TaskTimer(self.delay, self.__do_nothing)

        await asyncio.sleep(self.delay + 1)
        self.assertTrue(task_timer.task.done())

    async def test_cancel_task(self):
        """cancel後、タスクが動き続けておらず、キャンセルされているか"""

        task_timer = TaskTimer(self.delay, self.__do_nothing)
        task_timer.cancel()

        await asyncio.sleep(self.delay + 1)
        self.assertTrue(task_timer.task.cancelled())
        self.assertTrue(task_timer.task.done())

    async def test_no_execute_task(self):
        """タスクが動き続けているか"""
        task_timer = TaskTimer(self.delay, self.__do_nothing)

        await asyncio.sleep(0)
        self.assertFalse(task_timer.task.done())
        task_timer.cancel()

    async def test_cancel_task_multi(self):
        """複数回キャンセルしても問題ないか"""
        task_timer = TaskTimer(self.delay, self.__do_nothing)

        task_timer.cancel()

        # タスクがキャンセルされるのを待つ
        await asyncio.sleep(0.1)

        task_timer.cancel()

        await asyncio.sleep(0.1)

        self.assertTrue(task_timer.task.cancelled())
        self.assertTrue(task_timer.task.done())

    async def test_execution_time(self):
        """TaskTimerインスタンス作成時に適切にexecution_timeを初期化しているか"""
        task_timer = TaskTimer(self.delay, self.__do_nothing)
        now = time.time()
        self.assertTrue(now <= task_timer.execution_time <= now + self.delay)
        task_timer.cancel()

    async def test_return_value(self):
        """TaskTimerが引数有りでも正常に動作するか"""
        value = 1
        task_timer = TaskTimer(self.delay, self.__return_value, value)
        await asyncio.sleep(self.delay + 1)
        self.assertEqual(value, task_timer.task.result())
