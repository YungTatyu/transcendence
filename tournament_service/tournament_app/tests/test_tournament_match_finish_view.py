import pytest
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from django.utils.timezone import now

from tournament_app.models import Tournament
from tournament_app.utils.tournament_session import TournamentSession


@pytest.fixture
def tournament_setup_and_teardown(create_match_records_mocker):
    """
    トーナメントデータを作成し、後処理を実行(DBは別のfixtureで後処理)
    [INFO] TournamentSession.roundはregster時に1で初期化される
    """
    tournament_id = 1
    user_ids = [1, 2]
    Tournament.objects.create(tournament_id=tournament_id)
    TournamentSession.register(tournament_id, user_ids)
    round = TournamentSession.search(tournament_id).current_round

    yield (tournament_id, round)

    TournamentSession.clear()  # テスト後処理


class TestTournamentMatchFinish:
    def request_match_finish(self, client, status, tournament_id, round) -> dict:
        data = {"tournamentId": tournament_id, "round": round}
        response = client.post(
            "/tournaments/finish-match", data=data, content_type="application/json"
        )
        assert response.status_code == status
        return response.json()

    @pytest.mark.parametrize(
        "tournament_id, round, expect_status",
        [
            (1, 1, HTTP_200_OK),  # 正常
            (2, 1, HTTP_400_BAD_REQUEST),  # Tournamentレコードが存在しない
            (1, 2, HTTP_400_BAD_REQUEST),  # roundの整合性が取れない
        ],
    )
    @pytest.mark.django_db
    def test_finish_tournament_match(
        self, client, tournament_setup_and_teardown, tournament_id, round, expect_status
    ):
        self.request_match_finish(client, expect_status, tournament_id, round)

    @pytest.mark.django_db
    def test_tournament_session_does_not_exist(
        self, client, tournament_setup_and_teardown
    ):
        """TournamentSessionに情報が無い"""
        tournament_id, round = tournament_setup_and_teardown
        TournamentSession.clear()
        self.request_match_finish(client, HTTP_400_BAD_REQUEST, tournament_id, round)

    @pytest.mark.django_db
    def test_tournament_is_already_over(self, client, tournament_setup_and_teardown):
        """トーナメントがすでに終了している"""
        tournament_id, round = tournament_setup_and_teardown
        Tournament.objects.update(finish_date=now())
        self.request_match_finish(client, HTTP_400_BAD_REQUEST, tournament_id, round)
