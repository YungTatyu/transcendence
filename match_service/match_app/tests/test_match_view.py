import pytest
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from match_app.models import Match, MatchParticipant
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

        #  正常系の場合、レスポンスボディをassert
        if response.status_code == HTTP_200_OK:
            res_data = response.json()
            assert res_data["total"] == expect_total
            expect_offset = MatchSerializer.DEFAULT_OFFSET if offset is None else offset
            assert res_data["offset"] == expect_offset
            assert res_data["limit"] == expect_limit

        return response.json()

    def create_expect_result(self, match: Match) -> dict:
        participants = [
            {"id": participant.user_id, "score": participant.score}
            for participant in MatchParticipant.objects.filter(match_id=match)
        ]
        parent_match_id = (
            None if match.parent_match_id is None else match.parent_match_id.match_id
        )

        expect_result = {
            "matchId": match.match_id,
            "winnerUserId": match.winner_user_id,
            "mode": match.mode,
            "tournamentId": match.tournament_id,
            "parentMatchId": parent_match_id,
            "round": match.round,
            "participants": participants,
        }
        return expect_result

    @pytest.mark.django_db
    def test_simple_select(self, client, set_up_records):
        """
        INFO set_up_recordsにはMatchレコードが格納される
        検索条件無し
        totalは作成したMatchレコードの数とおなじになる
        """
        num_of_matches = len(set_up_records)
        expect_total = num_of_matches
        expect_limit = min(expect_total, MatchSerializer.DEFAULT_LIMIT)
        self.request_matches(client, HTTP_200_OK, expect_total, expect_limit)

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        "match_key, expect_total",
        [
            ("match1", 1),
            ("match2", 1),
        ],
    )
    def test_quick_play(self, client, set_up_records, match_key, expect_total):
        match_dict = set_up_records
        matchx = match_dict[match_key]
        expect_limit = min(expect_total, MatchSerializer.DEFAULT_LIMIT)
        res_data = self.request_matches(
            client, HTTP_200_OK, expect_total, expect_limit, match_id=matchx.match_id
        )
        results = res_data["results"]
        expect_results = [self.create_expect_result(matchx)]
        assert results == expect_results

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        "tournament_id, expect_total",
        [
            (1, 3),
            (2, 1),
            (3, 2),
        ],
    )
    def test_tournament(self, client, set_up_records, tournament_id, expect_total):
        expect_limit = min(expect_total, MatchSerializer.DEFAULT_LIMIT)
        res_data = self.request_matches(
            client, HTTP_200_OK, expect_total, expect_limit, tournament_id=tournament_id
        )
        results = res_data["results"]
        tournament_matches = Match.objects.filter(tournament_id=tournament_id)
        expect_results = [
            self.create_expect_result(match) for match in tournament_matches
        ]
        assert results == expect_results

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        "mode, expect_status",
        [
            ("QuickPlay", HTTP_200_OK),
            ("Tournament", HTTP_200_OK),
            ("Unknown", HTTP_400_BAD_REQUEST),  # modeが不正な値
        ],
    )
    def test_mode(self, client, set_up_records, mode, expect_status):
        """
        modeが指定したmodeと一致するレコードの数をテスト
        """
        match_dict = set_up_records
        expect_total = len(
            [match for match in match_dict.values() if match.mode == mode]
        )
        expect_limit = expect_total
        self.request_matches(
            client, expect_status, expect_total, expect_limit, mode=mode
        )

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        "offset, limit",
        [
            (2, None),  # ?offset=2
            (99, None),  # ?offset=99(offsetに指定する値がtotalよりも大きいケース)
            (None, 2),  # ?limit=2
            (None, 99),  # ?limit=99(limitに指定する値がtotalよりも大きいケース)
        ],
    )
    def test_offset_and_limit(self, client, set_up_records, offset, limit):
        """
        offsetとlimitを指定した際に正常に機能するかをテスト
        """
        num_of_matches = len(set_up_records)
        expect_total = num_of_matches
        if offset is not None:
            expect_limit = max(num_of_matches - offset, 0)
        else:
            expect_limit = min(num_of_matches, limit)
        self.request_matches(
            client, HTTP_200_OK, expect_total, expect_limit, offset=offset, limit=limit
        )

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
    @pytest.mark.parametrize(
        "winner_user_id",
        [
            (1),
            (2),
            (3),
            (4),
            (99),
        ],
    )
    def test_winner_user_id(self, client, set_up_records, winner_user_id):
        match_dict = set_up_records
        expect_total = len(
            [
                match
                for match in match_dict.values()
                if match.winner_user_id == winner_user_id
            ]
        )
        expect_limit = min(expect_total, MatchSerializer.DEFAULT_LIMIT)
        self.request_matches(
            client,
            HTTP_200_OK,
            expect_total,
            expect_limit,
            winner_user_id=winner_user_id,
        )

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        "round",
        [
            (1),
            (2),
            (3),
            (4),
            (99),
        ],
    )
    def test_round(self, client, set_up_records, round):
        match_dict = set_up_records
        expect_total = len(
            [match for match in match_dict.values() if match.round == round]
        )
        expect_limit = min(expect_total, MatchSerializer.DEFAULT_LIMIT)
        self.request_matches(
            client, HTTP_200_OK, expect_total, expect_limit, round=round
        )
