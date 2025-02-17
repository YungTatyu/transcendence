import pytest


@pytest.fixture()
def create_match_records_mocker(mocker):
    """"""
    return mocker.patch(
        "tournament_app.utils.tournament_session.TournamentSession._TournamentSession__create_match_records",
        return_value=None,
    )
