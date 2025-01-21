import time
import asyncio


class TaskTimer:
    """
    タスクとそのキャンセル可能期限を管理するクラス
    """

    def __init__(self, task: asyncio.Task, time_until_execution: int):
        """
        :param task: asyncio.Task インスタンス
        :param time_until_execution: タスクが実行されるまでの時間（秒）
        """
        self.__task = task
        # タスクが実行されるUNIX時刻
        self.__execution_time = time.time() + time_until_execution

    @property
    def execution_time(self) -> float:
        return self.__execution_time

    def cancel(self):
        """タスクが既に終了している場合にcancelしても何も起きない"""
        self.__task.cancel()
