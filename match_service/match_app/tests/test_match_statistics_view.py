import jwt
import pytest
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from match_app.models import Match, MatchParticipant


class TestMatchStatistics:
    def request_match_statistics(self, client, status, user_id):
        token_payload = {"user_id": 1}
        token = jwt.encode(token_payload, "secret_key", algorithm="HS256")
        client.cookies["access_token"] = token

        response = client.get(f"/matches/statistics/{user_id}")
        assert response.status_code == status
        return response.json()

    @pytest.mark.parametrize(
        "expect_code, user_id",
        [
            (HTTP_200_OK, 1),
            (HTTP_200_OK, 2),
            (HTTP_200_OK, 3),
            (HTTP_200_OK, 4),
            (HTTP_200_OK, 12345),  # 存在しないユーザーでも正常にレスポンスが返る
            (HTTP_400_BAD_REQUEST, "abcde"),  # user_idが数値でないなら400が返る
        ],
    )
    @pytest.mark.django_db
    def test_match_statistics(self, client, set_up_records, expect_code, user_id):
        res_data = self.request_match_statistics(client, expect_code, user_id)

        if expect_code == HTTP_200_OK:
            match_dict = set_up_records
            match_win_cnt = self.__get_match_win_count(match_dict, user_id)
            match_lose_cnt = self.__get_match_lose_count(match_dict, user_id)
            tournament_win_cnt = self.__get_tournament_winner_count(match_dict, user_id)

            expect_data = {
                "matchWinCount": match_win_cnt,
                "matchLoseCount": match_lose_cnt,
                "tournamentWinnerCount": tournament_win_cnt,
            }
            assert res_data == expect_data

    def __get_match_win_count(self, match_dict: dict[str, Match], user_id) -> int:
        cnt = 0
        for match in match_dict.values():
            if match.winner_user_id == user_id:
                cnt += 1
        return cnt

    def __get_match_lose_count(self, match_dict: dict[str, Match], user_id) -> int:
        cnt = 0
        for match in match_dict.values():
            if (
                MatchParticipant.objects.filter(
                    match_id=match, user_id=user_id
                ).exists()
                and match.winner_user_id is not None
                and match.winner_user_id != user_id
            ):
                cnt += 1
        return cnt

    def __get_tournament_winner_count(
        self, match_dict: dict[str, Match], user_id
    ) -> int:
        cnt = 0
        for match in match_dict.values():
            if (
                match.winner_user_id == user_id
                and match.mode == "Tournament"
                and match.parent_match_id is None
            ):
                cnt += 1
        return cnt
