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
        self.__execution_time = time.time() + time_until_execution

    @property
    def execution_time(self) -> float:
        return self.__execution_time

    def cancel(self):
        self.__task.cancel()
