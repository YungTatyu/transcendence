import asyncio
from typing import Optional
from .task_timer import TaskTimer


class TournamentMatchingManager:
    """
    トーナメントマッチングルームの人数を管理
    N秒後に強制的にトーナメントを開始させるためのタイマー管理
    """

    # dict[user_id, channel_name]
    _matching_wait_users: dict[int, str] = dict()
    # トーナメント強制開始用タイマーオブジェクト
    _task_timer = None

    @classmethod
    def get_matching_wait_users(cls) -> dict[int, str]:
        return cls._matching_wait_users

    @classmethod
    def add_matching_wait_users(cls, user_id: int, channel_name: str) -> int:
        # WARN 既に存在しているuser_idの場合、上書きされる
        cls._matching_wait_users[user_id] = channel_name
        return len(cls._matching_wait_users)

    @classmethod
    def del_matching_wait_user(cls, user_id: int) -> int:
        """存在しないuser_idを指定しても何も起きません"""
        cls._matching_wait_users.pop(user_id, None)
        return len(cls._matching_wait_users)

    @classmethod
    def clear_matching_wait_users(cls):
        cls._matching_wait_users.clear()

    @classmethod
    def set_task(cls, task: asyncio.Task, time_until_execution: int):
        # WARN タスクが終了していない状態で実行すると予期せぬ挙動になる
        cls._task_timer = TaskTimer(task, time_until_execution)

    @classmethod
    def cancel_task(cls):
        if cls._task_timer:
            cls._task_timer.cancel()
        cls._task_timer = None

    @classmethod
    def get_task_execution_time(cls) -> Optional[float]:
        """タイマーがない場合はNoneが返る"""
        if cls._task_timer:
            return cls._task_timer.execution_time
        return None
