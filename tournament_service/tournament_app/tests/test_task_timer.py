import asyncio
import time
from asyncio.exceptions import CancelledError, InvalidStateError

from django.test import TestCase

from tournament_app.utils.task_timer import TaskTimer


class TaskTimerTest(TestCase):
    delay = 1

    async def __async_raise_timeout_error(self):
        raise TimeoutError

    async def __return_value(self, value: int) -> int:
        return value

    async def test_execute_task(self):
        """タスクが正常終了し、意図した例外がスローされるか"""
        task_timer = TaskTimer(self.delay, self.__async_raise_timeout_error)

        try:
            await asyncio.sleep(self.delay + 1)
            task_timer.task.result()
        except Exception as e:
            self.assertIsInstance(e, TimeoutError)

    async def test_cancel_task(self):
        """cancel後、タスクが動き続けておらず、CancelledErrorがスローされるか"""

        task_timer = TaskTimer(self.delay, self.__async_raise_timeout_error)
        task_timer.cancel()

        try:
            await asyncio.sleep(self.delay + 1)
            task_timer.task.result()
        except asyncio.exceptions.CancelledError as e:
            self.assertIsInstance(e, CancelledError)
        except Exception as e:
            self.fail(e)

    async def test_no_execute_task(self):
        """タスクが終了しておらず、InvalidStateErrorがスローされるか"""
        task_timer = TaskTimer(self.delay, self.__async_raise_timeout_error)

        try:
            await asyncio.sleep(0)
            task_timer.task.result()
        except Exception as e:
            self.assertIsInstance(e, InvalidStateError)

    async def test_cancel_task_multi(self):
        """複数回キャンセルしても問題ないか"""
        task_timer = TaskTimer(self.delay, self.__async_raise_timeout_error)

        task_timer.cancel()

        # タスクがキャンセルされるのを待つ
        await asyncio.sleep(0.1)

        task_timer.cancel()

        await asyncio.sleep(0.1)

        self.assertTrue(task_timer.task.cancelled())

    async def test_execution_time(self):
        """TaskTimerインスタンス作成時に適切にexecution_timeを初期化しているか"""
        task_timer = TaskTimer(self.delay, self.__async_raise_timeout_error)
        now = time.time()
        self.assertTrue(now <= task_timer.execution_time <= now + self.delay)

    async def test_return_value(self):
        """TaskTimerが引数有りでも正常に動作するか"""
        value = 1
        task_timer = TaskTimer(self.delay, self.__return_value, value)
        await asyncio.sleep(self.delay + 1)
        self.assertEqual(value, task_timer.task.result())
