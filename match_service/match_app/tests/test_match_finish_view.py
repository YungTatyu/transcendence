import pytest
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

from match_app.client.vault_client import VaultClient
from match_app.models import Match, MatchParticipant

from .set_up_utils import (
    insert_match_participants_record,
    insert_quick_play_record,
    insert_tournament_record,
)


class TestMatchFinish:
    def request_match_finish(self, client, status, match_id, results) -> dict:
        """
        RequestBodyを作成し/matches/finish/エンドポイントを叩く
        正常系レスポンスならMatchとMatchParticipantレコードが作成されているかを確認
        """
        data = {"matchId": match_id, "results": results}
        api_key = VaultClient.fetch_api_key_not_required_token("matches")

        response = client.post(
            "/matches/finish",
            data=data,
            content_type="application/json",
            HTTP_X_API_KEY=api_key,
        )
        assert response.status_code == status

        #  正常系のレスポンスの場合、レスポンスボディもチェックする
        if response.status_code == HTTP_200_OK:
            match = Match.objects.filter(match_id=match_id).first()
            # トーナメント終了時、finish_dateは必ずセットされる
            assert match.finish_date is not None

            participants = MatchParticipant.objects.filter(match_id=match)
            user_ids = [result["userId"] for result in results]
            for participant in participants:
                user_id = participant.user_id
                # RequestBodyに含まれるuserIdでMatchParticipantレコードが作成されたか
                assert user_id in user_ids
                score = [
                    result["score"] for result in results if result["userId"] == user_id
                ][0]
                # RequestBodyに含まれるscoreでMatchParticipantレコードが作成されたか
                assert participant.score == score

        return response.json()

    def __insert_quick_play_match(self, user_ids: list[int]) -> int:
        """Matchレコードを1つ作成し、user_ids分のMatchParticipantレコードを作成"""
        match = insert_quick_play_record(None)
        match_id = match.match_id
        [insert_match_participants_record(match, user_id) for user_id in user_ids]
        return match_id

    def __insert_tournament_match(self, user_ids: list[int]) -> Match:
        """
        親試合を作成後、
        もう一つのMatchレコードを作成し、user_ids分のMatchParticipantレコードを作成
        """
        parent_match = insert_tournament_record(None, 1, None, 1)
        match = insert_tournament_record(None, 1, parent_match, 2)
        [insert_match_participants_record(match, user_id) for user_id in user_ids]
        return match

    @pytest.mark.parametrize(
        "user_ids, request_body",
        [
            ([1, 2], [{"userId": 1, "score": 11}, {"userId": 2, "score": 1}]),
        ],
    )
    @pytest.mark.django_db
    def test_simple_quick_play_match_finish(self, client, user_ids, request_body):
        """QuickPlayモードの試合が終了"""
        match_id = self.__insert_quick_play_match(user_ids)
        res_data = self.request_match_finish(
            client, HTTP_200_OK, match_id, request_body
        )
        assert res_data.get("finishDate", None) is not None

    @pytest.mark.parametrize(
        "user_ids, request_body",
        [
            ([1, 2], [{"userId": 1, "score": 11}, {"userId": 2, "score": 1}]),
        ],
    )
    @pytest.mark.django_db
    def test_simple_tournament_match_finish(
        self, request_finish_match_success_mocker, client, user_ids, request_body
    ):
        """Tournamentモードの試合が終了"""
        match = self.__insert_tournament_match(user_ids)
        match_id = match.match_id
        res_data = self.request_match_finish(
            client, HTTP_200_OK, match_id, request_body
        )
        assert res_data.get("finishDate", None) is not None

        # トーナメント試合が終了した際に勝者が親試合に登録されるか
        winner_user_id = max(request_body, key=lambda x: x["score"])["userId"]
        assert MatchParticipant.objects.filter(
            match_id=match.parent_match_id, user_id=winner_user_id
        ).exists()

    @pytest.mark.parametrize(
        "user_ids, request_body",
        [
            (  # 試合参加者が少ない
                [1, 2, 3],
                [{"userId": 2, "score": 1}, {"userId": 3, "score": 3}],
            ),
            (  # 試合参加者が多い
                [1, 2],
                [
                    {"userId": 1, "score": 11},
                    {"userId": 2, "score": 1},
                    {"userId": 3, "score": 3},
                ],
            ),
            (  # 試合参加者ではないユーザーが存在
                [1, 2],
                [{"userId": 100, "score": 11}, {"userId": 2, "score": 1}],
            ),
            (  # 空のリスト
                [1, 2],
                [],
            ),
            (  # 空のディクト
                [1, 2],
                [{}, {"userId": 2, "score": 1}],
            ),
            (  # 勝者が複数いる(最大のscoreが複数存在)
                [1, 2],
                [{"userId": 1, "score": 11}, {"userId": 2, "score": 11}],
            ),
            (  # １つの試合に同じユーザー参加してはいけない
                [1],
                [{"userId": 1, "score": 0}, {"userId": 1, "score": 11}],
            ),
        ],
    )
    @pytest.mark.django_db
    def test_faild_case(self, client, user_ids, request_body):
        match_id = self.__insert_quick_play_match(user_ids)
        self.request_match_finish(client, HTTP_400_BAD_REQUEST, match_id, request_body)

    @pytest.mark.django_db
    def test_not_exist_match(self, client):
        """レコードが存在しない試合"""
        not_exist_match_id = 12345
        results = [{"userId": 1, "score": 11}, {"userId": 2, "score": 1}]
        self.request_match_finish(
            client, HTTP_400_BAD_REQUEST, not_exist_match_id, results
        )

    @pytest.mark.django_db
    def test_already_finished(self, client):
        """試合は既に終了処理されている"""
        results = [
            {"userId": 1, "score": 0},
            {"userId": 2, "score": 11},
        ]
        user_ids = [result["userId"] for result in results]
        match_id = self.__insert_quick_play_match(user_ids)
        self.request_match_finish(client, HTTP_200_OK, match_id, results)
        # ２回目のfinish処理は不正
        self.request_match_finish(client, HTTP_400_BAD_REQUEST, match_id, results)

    @pytest.mark.django_db
    def test_faild_tournament_api_request(
        self, request_finish_match_error_mocker, client
    ):
        """
        TournamentAPIを叩く処理が失敗 + ロールバック処理のテスト
        """

        results = [{"userId": 1, "score": 11}, {"userId": 2, "score": 1}]
        user_ids = [result["userId"] for result in results]
        match = self.__insert_tournament_match(user_ids)
        match_id = match.match_id
        self.request_match_finish(
            client, HTTP_500_INTERNAL_SERVER_ERROR, match_id, results
        )

        for user_id in user_ids:
            match_participant_after_rollback = MatchParticipant.objects.filter(
                match_id=match_id, user_id=user_id
            ).first()
            assert match_participant_after_rollback.score is None

        match_after_rollback = Match.objects.filter(match_id=match_id).first()
        assert match_after_rollback.winner_user_id is None
        assert match_after_rollback.finish_date is None

        if match.parent_match_id is not None:
            winner_user_id = max(results, key=lambda x: x["score"])["userId"]
            assert not MatchParticipant.objects.filter(
                match_id=match.parent_match_id, user_id=winner_user_id
            ).exists()

    @pytest.mark.django_db
    def test_minus_one_score(self, client):
        """スコアに-1が許容されるかをテスト"""
        results = [
            {"userId": 1, "score": 0},
            {"userId": 2, "score": -1},
        ]
        user_ids = [result["userId"] for result in results]
        match_id = self.__insert_quick_play_match(user_ids)
        self.request_match_finish(client, HTTP_200_OK, match_id, results)

    @pytest.mark.django_db
    def test_minus_two_score(self, client):
        """
        スコアに-2が許容されないかをテスト
        INFO スコアの最小値は-1です
        """
        results = [
            {"userId": 1, "score": 0},
            {"userId": 2, "score": -2},
        ]
        user_ids = [result["userId"] for result in results]
        match_id = self.__insert_quick_play_match(user_ids)
        self.request_match_finish(client, HTTP_400_BAD_REQUEST, match_id, results)
