import pytest


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
