import asyncio


class TournamentMatchingManager:
    """
    トーナメントマッチングルームの人数を管理
    N秒後に強制的にトーナメントを開始させるためのタイマー管理
    """

    # dict[user_id, channel_name]
    _matching_wait_users: dict[int, str] = dict()
    # トーナメント強制開始用タイマーオブジェクト
    _task = None

    @classmethod
    def get_matching_wait_users(cls) -> dict[int, str]:
        return cls._matching_wait_users

    @classmethod
    def add_matching_wait_users(cls, user_id: int, channel_name: str) -> int:
        cls._matching_wait_users[user_id] = channel_name
        return len(cls._matching_wait_users)

    @classmethod
    def del_matching_wait_user(cls, user_id: int) -> int:
        cls._matching_wait_users.pop(user_id, None)
        return len(cls._matching_wait_users)

    @classmethod
    def clear_matching_wait_users(cls):
        cls._matching_wait_users.clear()

    @classmethod
    def set_task(cls, task: asyncio.Task):
        cls._task = task

    @classmethod
    def cancel_task(cls):
        if cls._task:
            cls._task.cancel()
        cls._task = None
