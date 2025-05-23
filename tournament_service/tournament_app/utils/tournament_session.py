from typing import Optional

from asgiref.sync import async_to_sync, sync_to_async

# from channels.layers import get_channel_layer
from django.conf import settings
from django.utils.timezone import now
from tournament_app.client.match_client import MatchClient
from tournament_app.consumers.tournament_state import TournamentState as State
from tournament_app.models import Tournament
from tournament_app.utils.task_timer import TaskTimer
from tournament_app.utils.tournament_tree import TournamentTree


class TournamentSession:
    __tournament_session_dict: dict[int, "TournamentSession"] = {}
    # INFO トーナメントの1試合を強制的に終了させるための時間
    LIMIT_TOURNAMENT_MATCH_SEC = 300

    def __init__(self, tournament_id: int, user_ids: list[int]):
        """
        [INFO] match作成処理失敗の場合、例外が発生、インスタンスは作成されない
        """
        self.__tournament_id: int = tournament_id
        self.__current_round: int = 1
        self.__user_ids: list[int] = user_ids
        self.__task_timer = None
        self.__create_match_records(tournament_id, user_ids)
        self.__matches_data = self.update_matches_data()
        async_to_sync(
            self.set_tournament_match_task,
            force_new_loop=False,
        )()

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

    def update_matches_data(self) -> dict:
        """
        matchesエンドポイントを叩き、tournament_idに紐づく試合データを取得
        TournamentSession.__matches_dataを更新
        """
        client = MatchClient(settings.MATCH_API_BASE_URL)

        response = client.fetch_matches_data(self.tournament_id)

        if response.status_code != 200:
            raise Exception

        return response.json()["results"]

    async def set_tournament_match_task(self):
        """
        トーナメント試合がいつまでも終わらない状況を防ぐ
        強制的に不戦勝処理を行うタスクをセット
        """
        # WARN タスクが終了していない状態で実行すると予期せぬ挙動になる
        self.__task_timer = TaskTimer(
            self.LIMIT_TOURNAMENT_MATCH_SEC, self.handle_tournament_match_bye
        )

    async def handle_tournament_match_bye(self):
        """
        時間内に試合が終了されなかった場合に不戦勝での勝ち上がり処理を実行
        """
        from tournament_app.consumers.tournament_consumer import TournamentConsumer

        current_match = [
            match for match in self.matches_data if match["round"] == self.current_round
        ][0]
        participant_ids = [p["id"] for p in current_match["participants"]]
        results = [{"userId": id, "score": -1} for id in participant_ids]
        results[0]["score"] = 0  # 一人だけscoreを0に設定し、不戦勝とする
        match_id = current_match["matchId"]
        client = MatchClient(settings.MATCH_API_BASE_URL)
        res_data = await client.fetch_tournament_match_finish(match_id, results)

        # MatchAPIを叩き、エラーの場合
        if res_data.get("error", None) is not None:
            # Error情報をSend
            await TournamentConsumer.broadcast_matches_info(
                State.ERROR,
                self.__tournament_id,
                self.__matches_data,
                self.__current_round,
            )
            # WebSocketを切断
            await TournamentConsumer.broadcast_force_disconnect(self.__tournament_id)
            # INFO 異常終了時、トーナメントは終了として扱う
            await sync_to_async(
                Tournament.objects.filter(tournament_id=self.__tournament_id).update,
                thread_sensitive=False,
            )(finish_date=now())
            TournamentSession.delete(self.__tournament_id)

    async def update_tournament_session_info(self):
        """
        トーナメント試合終了時に次の試合を行うための処理を実行する
        """
        from tournament_app.consumers.tournament_consumer import TournamentConsumer

        self.next_round()
        is_finished_tournament = self.current_round > len(self.matches_data)
        state = State.FINISHED if is_finished_tournament else State.ONGOING

        try:
            self.__matches_data = self.update_matches_data()
        except Exception:
            # MatchAPIを叩き、エラー場合、トーナメント終了&エラー情報をSend
            is_finished_tournament = True
            state = State.ERROR

        await TournamentConsumer.broadcast_matches_info(
            state, self.__tournament_id, self.__matches_data, self.__current_round
        )

        before_task = self.__task_timer

        # Tournament試合が存在するならTaskTimerをセット
        if not is_finished_tournament:
            await self.set_tournament_match_task()
        # トーナメントを終了、finish_dateを更新、WebSocket接続を切断
        else:
            await TournamentConsumer.broadcast_force_disconnect(self.__tournament_id)
            await sync_to_async(
                Tournament.objects.filter(tournament_id=self.__tournament_id).update,
                thread_sensitive=False,
            )(finish_date=now())
            TournamentSession.delete(self.__tournament_id)

        if before_task:
            # INFO タスクが既に終了している場合にcancelしても何も起きない
            before_task.cancel()
