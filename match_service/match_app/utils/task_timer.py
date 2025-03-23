import asyncio
import time
from collections.abc import Callable
from typing import Any, Optional


class TaskTimer:
    """
    タスクとそのキャンセル可能期限を管理するクラス
    INFO TournamentサービスのTaskTimerと同じなのでテストは記述していません
    """

    def __init__(self, sec: int, func: Callable, *args: Any):
        """
        :param sec: タスクが実行されるまでの時間（秒）
        :param func: タイマーをセットして実行したい関数
        :param args: funcに渡したい引数
        """
        self.__task = asyncio.create_task(self.__run_with_timer(sec, func, *args))
        # タスクが実行されるUNIX時刻
        self.__execution_time = time.time() + sec

    async def __run_with_timer(
        self, sec: int, func: Callable, *args: Any
    ) -> Optional[Any]:
        """
        指定した時間後に関数を実行する非同期タスク
        非同期タスクに戻り値が存在する場合、task.result()で取得可能
        """
        await asyncio.sleep(sec)
        return await func(*args)

    def cancel(self):
        # INFO タスクが既に終了している場合にcancelしても何も起きない
        self.__task.cancel()

    @property
    def execution_time(self) -> float:
        return self.__execution_time

    @property
    def task(self) -> asyncio.Task:
        return self.__task
