import pytest
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from match_app.client.vault_client import VaultClient
from match_app.models import Match, MatchParticipant


class TestTournamentMatch:
    def request_tournament_match(
        self, client, status, user_id_list, tournament_id, parent_match_id, round
    ) -> dict:
        data = {
            "userIdList": user_id_list,
            "tournamentId": tournament_id,
            "parentMatchId": parent_match_id,
            "round": round,
        }
        api_key = VaultClient.fetch_api_key_not_required_token("matches")

        response = client.post(
            "/matches/tournament-match",
            data=data,
            content_type="application/json",
            HTTP_X_API_KEY=api_key,
        )
        assert response.status_code == status

        #  正常系のレスポンスの場合、レスポンスボディもチェックする
        if response.status_code == HTTP_200_OK:
            match = Match.objects.filter(tournament_id=tournament_id).first()
            assert match.match_id >= 0  # match_idは0以上の値が自動で採番される
            assert match.winner_user_id is None  # nullがセットされる
            assert match.mode == "Tournament"
            assert match.start_date is None  # nullがセットされる
            assert match.finish_date is None  # nullがセットされる
            if parent_match_id is None:
                assert match.parent_match_id is None
            else:
                assert match.parent_match_id.match_id == parent_match_id
            assert match.round == round

            participants = MatchParticipant.objects.filter(match_id=match)
            # RequestBodyのuser_id_listとMatchParticipantのuser_idのリストが同じか
            assert len(user_id_list) == len(participants)
            for participant in participants:
                assert participant.user_id in user_id_list
                assert participant.score is None  # nullがセットされる

        return response.json()

    @pytest.mark.parametrize(
        "expect_code, user_ids, parent_match_id",
        [
            (HTTP_200_OK, [], None),  # 参加者が決まっていない試合は存在する
            (HTTP_200_OK, [1], None),  # 対戦相手が決まっていない試合は存在する
            (HTTP_200_OK, [1, 2], None),  # ２人の参加者
            (HTTP_200_OK, [1, 2, 3], None),  # 3人以上の参加者がいる試合は作成可能
            (HTTP_400_BAD_REQUEST, [1, 1], None),  # user_idが重複
            (HTTP_400_BAD_REQUEST, [1, 2], 12345),  # 指定した親試合が存在しない
        ],
    )
    @pytest.mark.django_db
    def test_tournament_match(self, client, expect_code, user_ids, parent_match_id):
        tournament_id = 1
        round = 1
        self.request_tournament_match(
            client, expect_code, user_ids, tournament_id, parent_match_id, round
        )

    @pytest.mark.django_db
    def test_have_parent_match(self, client):
        """親試合を持つ試合を作成"""
        res_data = self.request_tournament_match(client, HTTP_200_OK, [], 3, None, 3)
        parent_match_id = res_data["matchId"]
        self.request_tournament_match(
            client, HTTP_200_OK, [3, 4], 2, parent_match_id, 2
        )
        self.request_tournament_match(
            client, HTTP_200_OK, [1, 2], 1, parent_match_id, 1
        )

    @pytest.mark.django_db
    def test_same_tournament_id_and_round(self, client):
        """同一のtournament_idとroundを持つ試合は作成不可"""
        tournament_id = 1
        round = 1
        self.request_tournament_match(
            client, HTTP_200_OK, [3, 4], tournament_id, None, round
        )
        self.request_tournament_match(
            client, HTTP_400_BAD_REQUEST, [1, 2], tournament_id, None, round
        )
