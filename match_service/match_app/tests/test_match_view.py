import pytest
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from match_app.serializers import MatchSerializer

from .set_up_utils import create_query_string


class TestMatchView:
    @staticmethod
    def request_matches(
        client,
        status,
        expect_total,
        expect_limit,
        match_id=None,
        winner_user_id=None,
        mode=None,
        tournament_id=None,
        round=None,
        offset=None,
        limit=None,
    ) -> dict:
        """
        1. 引数で受け取るNoneではないパラメータを用いてQueryStringを作成
        2. /matches/ エンドポイントへリクエストを送信
        3. 正常なレスポンスであれば、total, offset, limitの値をチェック
        INFO レスポンスのoffsetはQueryStringでの指定があればその値、なければ0が返る
        """
        query_string = create_query_string(
            matchId=match_id,
            winnerUserId=winner_user_id,
            mode=mode,
            tournamentId=tournament_id,
            round=round,
            offset=offset,
            limit=limit,
        )
        response = client.get(f"/matches{query_string}")

        assert response.status_code == status

        if response.status_code == HTTP_200_OK:
            res_data = response.json()
            assert res_data["total"] == expect_total
            expect_offset = MatchSerializer.DEFAULT_OFFSET if offset is None else offset
            assert res_data["offset"] == expect_offset
            assert res_data["limit"] == expect_limit

        return response.json()

    @pytest.mark.django_db
    def test_simple_select(self, client, set_up_records):
        """
        INFO set_up_recordsにはMatchレコードの数が格納される
        検索条件無し
        totalは作成したMatchレコードの数とおなじになる
        """
        num_of_matches = len(set_up_records)
        expect_total = num_of_matches
        expect_limit = min(expect_total, MatchSerializer.DEFAULT_LIMIT)
        self.request_matches(client, HTTP_200_OK, expect_total, expect_limit)

    @pytest.mark.django_db
    def test_finished_quick_play_results(self, client, set_up_records):
        """
        .set_up_records.__insert_finished_quick_playで作成されるレコードを対象にテスト
        """
        match_id_dict = set_up_records
        match1_id = match_id_dict["match1_id"]
        expect_total = 1
        expect_limit = min(expect_total, MatchSerializer.DEFAULT_LIMIT)
        res_data = self.request_matches(
            client, HTTP_200_OK, expect_total, expect_limit, match_id=match1_id
        )
        results = res_data["results"]
        expect_results = [
            {
                "matchId": match_id_dict["match1_id"],
                "winnerUserId": 3,
                "mode": "QuickPlay",
                "tournamentId": None,
                "parentMatchId": None,
                "round": None,
                "participants": [
                    {"id": 3, "score": 11},
                    {"id": 4, "score": 5},
                ],
            },
        ]
        assert results == expect_results

    @pytest.mark.django_db
    def test_not_finished_quick_play_results(self, client, set_up_records):
        """
        .set_up_records.__insert_not_finished_quick_playで作成されるレコードを対象にテスト
        """
        match_id_dict = set_up_records
        match2_id = match_id_dict["match2_id"]
        expect_total = 1
        expect_limit = min(expect_total, MatchSerializer.DEFAULT_LIMIT)
        res_data = self.request_matches(
            client, HTTP_200_OK, expect_total, expect_limit, match_id=match2_id
        )
        results = res_data["results"]
        expect_results = [
            {
                "matchId": match2_id,
                "winnerUserId": None,
                "mode": "QuickPlay",
                "tournamentId": None,
                "parentMatchId": None,
                "round": None,
                "participants": [
                    {"id": 1, "score": None},
                    {"id": 2, "score": None},
                ],
            },
        ]
        assert results == expect_results

    @pytest.mark.django_db
    def test_not_finished_tournament_results(self, client, set_up_records):
        """
        .set_up_records.__insert_not_finished_tournamentで作成されるレコードを対象にテスト
        """
        match_id_dict = set_up_records
        tournament_id = 1
        expect_total = 3
        expect_limit = min(expect_total, MatchSerializer.DEFAULT_LIMIT)
        res_data = self.request_matches(
            client, HTTP_200_OK, expect_total, expect_limit, tournament_id=tournament_id
        )
        results = res_data["results"]
        expect_results = [
            {
                "matchId": match_id_dict["match3_id"],
                "winnerUserId": None,
                "mode": "Tournament",
                "tournamentId": tournament_id,
                "parentMatchId": None,
                "round": 3,
                "participants": [],
            },
            {
                "matchId": match_id_dict["match4_id"],
                "winnerUserId": None,
                "mode": "Tournament",
                "tournamentId": tournament_id,
                "parentMatchId": match_id_dict["match3_id"],
                "round": 2,
                "participants": [
                    {"id": 3, "score": None},
                    {"id": 4, "score": None},
                ],
            },
            {
                "matchId": match_id_dict["match5_id"],
                "winnerUserId": None,
                "mode": "Tournament",
                "tournamentId": tournament_id,
                "parentMatchId": match_id_dict["match3_id"],
                "round": 1,
                "participants": [
                    {"id": 1, "score": None},
                    {"id": 2, "score": None},
                ],
            },
        ]
        assert results == expect_results

    @pytest.mark.django_db
    def test_finished_tournament_results(self, client, set_up_records):
        """
        .set_up_records.__insert_finished_tournamentで作成されるレコードを対象にテスト
        """
        match_id_dict = set_up_records
        tournament_id = 2
        expect_total = 1
        expect_limit = min(expect_total, MatchSerializer.DEFAULT_LIMIT)
        res_data = self.request_matches(
            client, HTTP_200_OK, expect_total, expect_limit, tournament_id=tournament_id
        )
        results = res_data["results"]
        expect_results = [
            {
                "matchId": match_id_dict["match6_id"],
                "winnerUserId": 1,
                "mode": "Tournament",
                "tournamentId": tournament_id,
                "parentMatchId": None,
                "round": 1,
                "participants": [
                    {"id": 1, "score": 11},
                    {"id": 2, "score": 0},
                ],
            },
        ]
        assert results == expect_results

    @pytest.mark.django_db
    def test_only_one_round_finished_tournament_results(self, client, set_up_records):
        """
        .set_up_records.__insert_only_one_round_finished_tournamentで作成されるレコードを対象にテスト
        """
        match_id_dict = set_up_records
        tournament_id = 3
        expect_total = 2
        expect_limit = min(expect_total, MatchSerializer.DEFAULT_LIMIT)
        res_data = self.request_matches(
            client, HTTP_200_OK, expect_total, expect_limit, tournament_id=tournament_id
        )
        results = res_data["results"]
        expect_results = [
            {
                "matchId": match_id_dict["match7_id"],
                "winnerUserId": None,
                "mode": "Tournament",
                "tournamentId": tournament_id,
                "parentMatchId": None,
                "round": 2,
                "participants": [
                    {"id": 1, "score": None},
                    {"id": 3, "score": None},
                ],
            },
            {
                "matchId": match_id_dict["match8_id"],
                "winnerUserId": 1,
                "mode": "Tournament",
                "tournamentId": tournament_id,
                "parentMatchId": match_id_dict["match7_id"],
                "round": 1,
                "participants": [
                    {"id": 1, "score": 11},
                    {"id": 2, "score": 0},
                ],
            },
        ]
        assert results == expect_results

    @pytest.mark.django_db
    def test_not_exist_match_id(self, client, set_up_records):
        """存在しないmatch_idの場合、エラーでなく、空のresultsを返す"""
        match_id = 12345
        expect_total = 0
        expect_limit = 0
        res_data = self.request_matches(
            client, HTTP_200_OK, expect_total, expect_limit, match_id=match_id
        )
        assert res_data["results"] == []

    @pytest.mark.django_db
    def test_winner_user_id(self, client, set_up_records):
        winner_user_id = 1
        expect_total = 2
        expect_limit = 2
        self.request_matches(
            client,
            HTTP_200_OK,
            expect_total,
            expect_limit,
            winner_user_id=winner_user_id,
        )

    @pytest.mark.django_db
    def test_quick_play_mode(self, client, set_up_records):
        mode = "QuickPlay"
        expect_total = 2
        expect_limit = 2
        self.request_matches(client, HTTP_200_OK, expect_total, expect_limit, mode=mode)

    @pytest.mark.django_db
    def test_tournament_mode(self, client, set_up_records):
        mode = "Tournament"
        expect_total = 6
        expect_limit = 6
        self.request_matches(client, HTTP_200_OK, expect_total, expect_limit, mode=mode)

    @pytest.mark.django_db
    def test_unknown_mode(self, client, set_up_records):
        """modeにはQuickPlayかTournamentしか指定できない"""
        mode = "Unknown"
        self.request_matches(client, HTTP_400_BAD_REQUEST, None, None, mode=mode)

    @pytest.mark.django_db
    def test_round(self, client, set_up_records):
        round = 1
        expect_total = 3
        expect_limit = 3
        self.request_matches(
            client, HTTP_200_OK, expect_total, expect_limit, round=round
        )

    @pytest.mark.django_db
    def test_offset(self, client, set_up_records):
        """
        num_of_matches == 作成したMatchレコードの数
        expect_total == 作成したMatchレコードの数(QueryStringでoffset以外の条件を入れていないため)
        expect_limit == 全体のレコード数からoffset分ずらした値
        """
        num_of_matches = len(set_up_records)
        offset = 2
        expect_total = num_of_matches
        expect_limit = max(num_of_matches - offset, 0)
        self.request_matches(
            client, HTTP_200_OK, expect_total, expect_limit, offset=offset
        )

    @pytest.mark.django_db
    def test_offset_over_total(self, client, set_up_records):
        """
        全体のレコード数よりもoffsetが大きいため、resultsは空
        """
        num_of_matches = len(set_up_records)
        offset = num_of_matches + 1
        expect_total = num_of_matches
        expect_limit = max(num_of_matches - offset, 0)
        res_data = self.request_matches(
            client, HTTP_200_OK, expect_total, expect_limit, offset=offset
        )
        assert res_data["results"] == []

    @pytest.mark.django_db
    def test_limit(self, client, set_up_records):
        """全体のレコード数がlimitを超える場合、limitの値がlimitとして返される"""
        num_of_matches = len(set_up_records)
        limit = 2
        expect_total = num_of_matches
        expect_limit = min(num_of_matches, limit)
        self.request_matches(
            client, HTTP_200_OK, expect_total, expect_limit, limit=limit
        )

    @pytest.mark.django_db
    def test_limit_over_total(self, client, set_up_records):
        """limitが全体のレコード数を超える場合、全体のレコード数がlimitとして返る"""
        num_of_matches = len(set_up_records)
        limit = num_of_matches + 1
        expect_total = num_of_matches
        expect_limit = min(num_of_matches, limit)
        self.request_matches(
            client, HTTP_200_OK, expect_total, expect_limit, limit=limit
        )
