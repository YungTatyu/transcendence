import asyncio
from typing import Optional


class QuickPlayMatchingManager:
    """
    QuickPlayマッチングルームの人数を管理
    INFO TournamentMatchingManagerからTaskTimer機能を除去したものと同じ
         そのため、このクラスのテストは作成しない
    """

    # dict[user_id, channel_name]
    __waiting_users: dict[int, str] = dict()
    # 非同期排他制御用のlockオブジェクト
    __lock: Optional[asyncio.Lock] = None  # 初期化を遅延させるためNoneを設定

    @classmethod
    def get_waiting_users(cls) -> dict[int, str]:
        return cls.__waiting_users

    @classmethod
    def add_user(cls, user_id: int, channel_name: str) -> int:
        # WARN 既に存在しているuser_idの場合、上書きされる
        cls.__waiting_users[user_id] = channel_name
        return len(cls.__waiting_users)

    @classmethod
    def del_user(cls, user_id: int) -> int:
        """存在しないuser_idを指定しても何も起きません"""
        cls.__waiting_users.pop(user_id, None)
        return len(cls.__waiting_users)

    @classmethod
    def clear_waiting_users(cls):
        cls.__waiting_users.clear()

    @classmethod
    async def get_lock(cls) -> asyncio.Lock:
        if cls.__lock is None:
            cls.__lock = asyncio.Lock()  # イベントループ内で初期化
        return cls.__lock
