import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from tournament_app.utils.tournament_session import TournamentSession


@pytest.fixture()
def create_match_records_mocker(mocker):
    """"""
    return mocker.patch(
        "tournament_app.utils.tournament_session.TournamentSession._TournamentSession__create_match_records",
        return_value=None,
    )


@pytest.fixture()
def create_match_records_error_mocker(mocker):
    """"""
    return mocker.patch(
        "tournament_app.utils.tournament_session.TournamentSession._TournamentSession__create_match_records",
        side_effect=Exception,
    )


@pytest.fixture()
def update_matches_data_mocker(mocker):
    """"""
    return mocker.patch(
        "tournament_app.utils.tournament_session.TournamentSession.update_matches_data",
        side_effect=None,
    )


@pytest.fixture()
def dummy_matches_data_start_mocker(mocker):
    """
    参加者2人の場合のmatches_dataをreturn
    """
    dummy_matches_data = {
        "matches_data": [
            {
                "matchId": 2,
                "winnerUserId": 40014,
                "mode": "Tournament",
                "tournamentId": 1,
                "parentMatchId": None,
                "round": 1,
                "participants": [
                    {"id": 40014, "score": None},
                    {"id": 40046, "score": None},
                ],
            },
        ],
        "current_round": 1,
        "state": "ongoing",
    }
    return mocker.patch(
        "tournament_app.utils.tournament_session.TournamentSession.update_matches_data",
        return_value=dummy_matches_data,
    )


@pytest.fixture()
def dummy_matches_data_end_mocker(mocker):
    """
    参加者2人の場合のmatches_dataをreturn
    """
    dummy_matches_data = {
        "matches_data": [
            {
                "matchId": 2,
                "winnerUserId": 40014,
                "mode": "Tournament",
                "tournamentId": 1,
                "parentMatchId": None,
                "round": 1,
                "participants": [{"id": 40014, "score": 0}, {"id": 40046, "score": -1}],
            },
        ],
        "current_round": 2,
        "state": "finished",
    }
    return mocker.patch(
        "tournament_app.utils.tournament_session.TournamentSession.update_matches_data",
        return_value=dummy_matches_data,
    )


@pytest.fixture()
def mock_limit_tournament_match_sec(mocker):
    """TournamentSession.LIMIT_TOURNAMENT_MATCH_SEC をモックして値を変更"""
    mocker.patch.object(TournamentSession, "LIMIT_TOURNAMENT_MATCH_SEC", 1)


@pytest.fixture
def mock_handle_tournament_match_bye():
    with patch.object(
        TournamentSession,
        "handle_tournament_match_bye",
        new=TournamentSession.update_tournament_session_info,
    ):
        yield
