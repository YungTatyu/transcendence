from collections.abc import Callable
from typing import Any, Optional
from .task_timer import TaskTimer


class TournamentMatchingManager:
    """
    トーナメントマッチングルームの人数を管理
    N秒後に強制的にトーナメントを開始させるためのタイマー管理
    """

    # dict[user_id, channel_name]
    __matching_wait_users: dict[int, str] = dict()
    # トーナメント強制開始用タイマーオブジェクト
    __task_timer = None

    @classmethod
    def get_matching_wait_users(cls) -> dict[int, str]:
        return cls.__matching_wait_users

    @classmethod
    def add_matching_wait_users(cls, user_id: int, channel_name: str) -> int:
        # WARN 既に存在しているuser_idの場合、上書きされる
        cls.__matching_wait_users[user_id] = channel_name
        return len(cls.__matching_wait_users)

    @classmethod
    def del_matching_wait_user(cls, user_id: int) -> int:
        """存在しないuser_idを指定しても何も起きません"""
        cls.__matching_wait_users.pop(user_id, None)
        return len(cls.__matching_wait_users)

    @classmethod
    def clear_matching_wait_users(cls):
        cls.__matching_wait_users.clear()

    @classmethod
    def set_task(cls, sec: int, task: Callable, *args: Any):
        # WARN タスクが終了していない状態で実行すると予期せぬ挙動になる
        cls.__task_timer = TaskTimer(sec, task, *args)

    @classmethod
    def get_task(cls) -> Optional[TaskTimer]:
        return cls.__task_timer

    @classmethod
    def cancel_task(cls):
        if cls.__task_timer:
            cls.__task_timer.cancel()
        cls.__task_timer = None

    @classmethod
    def get_task_execution_time(cls) -> Optional[float]:
        """タイマーがない場合はNoneが返る"""
        if cls.__task_timer:
            return cls.__task_timer.execution_time
        return None
