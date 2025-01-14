import asyncio


class TournamentMatchingManager:
    # ルーム全体の待機ユーザー数を管理
    _matching_wait_users: set[str] = set()
    # トーナメント強制開始用タイマーオブジェクト
    _timer = None

    @staticmethod
    def get_matching_wait_users():
        return TournamentMatchingManager._matching_wait_users

    @staticmethod
    def append_matching_wait_users(user_id: str) -> int:
        TournamentMatchingManager._matching_wait_users.add(user_id)
        return len(TournamentMatchingManager._matching_wait_users)

    @staticmethod
    def del_matching_wait_user(user_id: str) -> int:
        TournamentMatchingManager._matching_wait_users.discard(user_id)
        return len(TournamentMatchingManager._matching_wait_users)

    @staticmethod
    def clear_matching_wait_users():
        TournamentMatchingManager._matching_wait_users.clear()

    @staticmethod
    def set_timer(task: asyncio.Task):
        TournamentMatchingManager._timer = task

    @staticmethod
    def cancel_timer():
        if TournamentMatchingManager._timer:
            TournamentMatchingManager._timer.cancel()
        TournamentMatchingManager._timer = None
