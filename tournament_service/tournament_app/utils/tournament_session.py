from typing import Optional

from channels.layers import get_channel_layer
from django.conf import settings
from tournament_app.utils.match_client import MatchClient
from tournament_app.utils.task_timer import TaskTimer
from tournament_app.utils.tournament_tree import TournamentTree


class TournamentSession:
    __tournament_session_dict: dict[int, "TournamentSession"] = {}
    LIMIT_TOURNAMENT_MATCH_SEC = 300

    def __init__(self, tournament_id: int, user_ids: list[int]):
        """
        [INFO] match作成処理失敗の場合、例外が発生、インスタンスは作成されない
        """
        self.__tournament_id: int = tournament_id
        self.__current_round: int = 1
        self.__user_ids: list[int] = user_ids
        self.__matches_data = {}
        self.__task_timer = None
        self.__create_match_records(tournament_id, user_ids)
        self.update_matches_data()

    @classmethod
    def register(
        cls, tournament_id: int, user_ids: list[int]
    ) -> Optional["TournamentSession"]:
        """
        (既にセッションが存在 OR match作成処理失敗) => return None
        [INFO] match作成処理失敗の場合、registerされない
        """
        if tournament_id in cls.__tournament_session_dict:
            return None
        try:
            tournament_session = TournamentSession(tournament_id, user_ids)
            cls.__tournament_session_dict[tournament_id] = tournament_session
            return tournament_session
        except Exception:
            return None

    @classmethod
    def search(cls, tournament_id: int) -> Optional["TournamentSession"]:
        return cls.__tournament_session_dict.get(tournament_id, None)

    @classmethod
    def delete(cls, tournament_id: int) -> bool:
        if cls.search(tournament_id):
            del cls.__tournament_session_dict[tournament_id]
            return True
        return False

    @classmethod
    def clear(cls):
        cls.__tournament_session_dict.clear()

    @property
    def tournament_id(self) -> int:
        return self.__tournament_id

    @property
    def user_ids(self) -> list[int]:
        return self.__user_ids

    @property
    def current_round(self) -> int:
        return self.__current_round

    @property
    def matches_data(self) -> dict:
        return self.__matches_data

    def next_round(self) -> int:
        self.__current_round += 1
        return self.__current_round

    def __create_match_records(self, tournament_id: int, user_ids: list[int]):
        """
        matchesサーバのAPIを叩き、レコードを作成する処理
        [WARN] matchAPIを叩く処理でエラーが発生した場合、例外が発生
        """
        tree = TournamentTree(user_ids)
        client = MatchClient(settings.MATCH_API_BASE_URL)

        for node in TournamentTree.bfs_iterator(tree.root):
            parent = node.parent_node
            parent_match_id = None if parent is None else parent.match_id
            response = client.create_tournament_match_record(
                node.value_list, tournament_id, parent_match_id, node.round
            )

            if response.status_code != 200:
                raise Exception
            node.match_id = int(response.json()["matchId"])

    def update_matches_data(self):
        client = MatchClient(settings.MATCH_API_BASE_URL)

        response = client.fetch_matches_data(self.tournament_id)

        if response.status_code != 200:
            raise Exception

        self.__matches_data = response.json()["results"]

    async def set_tournament_match_task(self):
        # WARN タスクが終了していない状態で実行すると予期せぬ挙動になる
        self.__task_timer = TaskTimer(
            self.LIMIT_TOURNAMENT_MATCH_SEC, self.handle_tournament_match_bye
        )

    def cancel_tournament_match_task(self):
        if self.__task_timer:
            self.__task_timer.cancel()
        self.__task_timer = None

    async def handle_tournament_match_bye(self):
        # TODO トーナメントが不戦勝の場合の処理を記述する
        current_match = [
            match for match in self.matches_data if match["round"] == self.current_round
        ][0]
        participant_ids = [p["id"] for p in current_match["participants"]]
        results = [{"userId": id, "score": 0} for id in participant_ids]
        results[0]["score"] = 11
        match_id = current_match["matchId"]
        client = MatchClient(settings.MATCH_API_BASE_URL)
        await client.fetch_tournament_match_finish(match_id, results)

    async def update_tournament_session_info(self):
        """
        トーナメントの情報を更新し、次の試合のアナウンスメントイベントを発生させる
        """
        from tournament_app.consumers.tournament_consumer import TournamentConsumer

        self.update_matches_data()

        # 更新されたmatches_dataをTournamentグループに対してブロードキャスト
        channel_layer = get_channel_layer()
        group_name = TournamentConsumer.get_group_name(self.__tournament_id)
        await channel_layer.group_send(
            group_name,
            {
                "type": "send_matches_data",  # TournamentConsumer.send_matches_data
                "matches_data": self.__matches_data,
            },
        )
        self.next_round()

        before_task = self.__task_timer

        # Tournament試合が存在するならTaskTimerをセット
        if self.current_round <= len(self.matches_data):
            await self.set_tournament_match_task()

        if before_task:
            before_task.cancel()
