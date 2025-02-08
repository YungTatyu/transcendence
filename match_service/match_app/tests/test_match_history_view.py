import pytest
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from match_app.serializers import MatchHistorySerializer

from .set_up_utils import create_query_string


class TestMatchHistory:
    @staticmethod
    def request_match_histories(
        client, status, user_id, expect_total, expect_limit, offset=None, limit=None
    ) -> dict:
        query_string = create_query_string(offset=offset, limit=limit)
        response = client.get(f"/matches/histories/{user_id}{query_string}")
        assert response.status_code == status

        #  正常系レスポンスの場合、レスポンスボディもチェックする
        if response.status_code == HTTP_200_OK:
            res_data = response.json()
            assert res_data["total"] == expect_total
            expect_offset = (
                MatchHistorySerializer.DEFAULT_OFFSET if offset is None else offset
            )
            assert res_data["offset"] == expect_offset
            assert res_data["limit"] == expect_limit

        return response.json()

    @staticmethod
    def assert_result(result, mode, win_or_lose, user_score, opponents):
        assert result["mode"] == mode
        assert result["result"] == win_or_lose
        assert result["date"] is not None
        assert result["userScore"] == user_score
        assert result["opponents"][0] == opponents

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        "user_id, expect_total, mode, win_or_lose, user_score, opponent_data",
        [
            (1, 2, "Tournament", "win", 11, {"id": 2, "score": 0}),
            (2, 2, "Tournament", "lose", 0, {"id": 1, "score": 11}),
            (3, 1, "QuickPlay", "win", 11, {"id": 4, "score": 5}),
            (4, 1, "QuickPlay", "lose", 5, {"id": 3, "score": 11}),
        ],
    )
    def test_userx(
        self,
        client,
        set_up_records,
        user_id,
        expect_total,
        mode,
        win_or_lose,
        user_score,
        opponent_data,
    ):
        expect_limit = min(expect_total, MatchHistorySerializer.DEFAULT_LIMIT)
        res_data = self.request_match_histories(
            client, HTTP_200_OK, user_id, expect_total, expect_limit
        )

        for result in res_data["results"]:
            self.assert_result(result, mode, win_or_lose, user_score, opponent_data)

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        "expect_limit, offset, limit",
        [
            (1, 1, None),  # ?offset=1
            (1, None, 1),  # ?limit=1
            (0, 3, None),  # ?offset=3(offset over total)
            (2, None, 3),  # ?limit=3(limit over total)
            (1, 1, 1),  # ?offset=1&limit=1
            (1, 1, 10),  # ?offset=1&limit=10(limit over total)
        ],
    )
    def test_offset_and_limit(
        self, client, set_up_records, expect_limit, offset, limit
    ):
        user_id = 1
        expect_total = 2
        self.request_match_histories(
            client,
            HTTP_200_OK,
            user_id,
            expect_total,
            expect_limit,
            offset=offset,
            limit=limit,
        )

    @pytest.mark.django_db
    def test_user_not_exist(self, client, set_up_records):
        """存在しないユーザーでも正常にレスポンスが返る"""
        not_exist_user_id = 12345
        expect_total = 0
        expect_limit = min(expect_total, MatchHistorySerializer.DEFAULT_LIMIT)
        res_data = self.request_match_histories(
            client, HTTP_200_OK, not_exist_user_id, expect_total, expect_limit
        )
        assert res_data["results"] == []

    @pytest.mark.django_db
    def test_user_id_is_not_digit(self, client, set_up_records):
        """URLのPathのuser_idが数値でないなら400が返る"""
        not_digit_user_id = "abcde"
        self.request_match_histories(
            client, HTTP_400_BAD_REQUEST, not_digit_user_id, None, None
        )
