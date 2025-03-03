import pytest
import requests
from unittest.mock import patch, MagicMock

from tournament_app.utils.tournament_session import TournamentSession


@pytest.fixture()
def create_match_records_mocker(mocker):
    """TournamentSession.__create_match_recordsをNoneを返すだけの処理でモック"""
    return mocker.patch(
        "tournament_app.utils.tournament_session.TournamentSession._TournamentSession__create_match_records",
        return_value=None,
    )


@pytest.fixture()
def create_match_records_error_mocker(mocker):
    """TournamentSession.__create_match_recordsを例外を発生させる処理でモック"""
    return mocker.patch(
        "tournament_app.utils.tournament_session.TournamentSession._TournamentSession__create_match_records",
        side_effect=Exception,
    )


@pytest.fixture()
def dummy_matches_data_mocker(mocker):
    """
    参加者4人の場合の試合状況をreturnする
    [INFO] 呼び出すたびに、データを順番に返すイテレータみたいな処理です
    """
    dummy_matches_data_list = [
        {  # 試合開始時
            "matches_data": [
                {
                    "matchId": 1,
                    "winnerUserId": None,
                    "mode": "Tournament",
                    "tournamentId": 1,
                    "parentMatchId": None,
                    "round": 3,
                    "participants": [],
                },
                {
                    "matchId": 2,
                    "winnerUserId": None,
                    "mode": "Tournament",
                    "tournamentId": 1,
                    "parentMatchId": 1,
                    "round": 1,
                    "participants": [
                        {"id": 51574, "score": None},
                        {"id": 51592, "score": None},
                    ],
                },
                {
                    "matchId": 3,
                    "winnerUserId": None,
                    "mode": "Tournament",
                    "tournamentId": 1,
                    "parentMatchId": 1,
                    "round": 2,
                    "participants": [
                        {"id": 51590, "score": None},
                        {"id": 36858, "score": None},
                    ],
                },
            ],
            "current_round": 1,
            "state": "ongoing",
        },
        {  # round1終了時
            "matches_data": [
                {
                    "matchId": 1,
                    "winnerUserId": None,
                    "mode": "Tournament",
                    "tournamentId": 1,
                    "parentMatchId": None,
                    "round": 3,
                    "participants": [
                        {"id": 51574, "score": None},
                    ],
                },
                {
                    "matchId": 2,
                    "winnerUserId": 51574,
                    "mode": "Tournament",
                    "tournamentId": 1,
                    "parentMatchId": 1,
                    "round": 1,
                    "participants": [
                        {"id": 51574, "score": 0},
                        {"id": 51592, "score": -1},
                    ],
                },
                {
                    "matchId": 3,
                    "winnerUserId": None,
                    "mode": "Tournament",
                    "tournamentId": 1,
                    "parentMatchId": 1,
                    "round": 2,
                    "participants": [
                        {"id": 51590, "score": None},
                        {"id": 36858, "score": None},
                    ],
                },
            ],
            "current_round": 2,
            "state": "ongoing",
        },
        {  # round2終了時
            "matches_data": [
                {
                    "matchId": 1,
                    "winnerUserId": None,
                    "mode": "Tournament",
                    "tournamentId": 1,
                    "parentMatchId": None,
                    "round": 3,
                    "participants": [
                        {"id": 51574, "score": None},
                        {"id": 51590, "score": None},
                    ],
                },
                {
                    "matchId": 2,
                    "winnerUserId": 51574,
                    "mode": "Tournament",
                    "tournamentId": 1,
                    "parentMatchId": 1,
                    "round": 1,
                    "participants": [
                        {"id": 51574, "score": 0},
                        {"id": 51592, "score": -1},
                    ],
                },
                {
                    "matchId": 3,
                    "winnerUserId": 51590,
                    "mode": "Tournament",
                    "tournamentId": 1,
                    "parentMatchId": 1,
                    "round": 2,
                    "participants": [
                        {"id": 51590, "score": 0},
                        {"id": 36858, "score": -1},
                    ],
                },
            ],
            "current_round": 3,
            "state": "ongoing",
        },
        {  # round3終了時(トーナメント終了時)
            "matches_data": [
                {
                    "matchId": 1,
                    "winnerUserId": 51574,
                    "mode": "Tournament",
                    "tournamentId": 1,
                    "parentMatchId": None,
                    "round": 3,
                    "participants": [
                        {"id": 51574, "score": 0},
                        {"id": 51590, "score": -1},
                    ],
                },
                {
                    "matchId": 2,
                    "winnerUserId": 51574,
                    "mode": "Tournament",
                    "tournamentId": 1,
                    "parentMatchId": 1,
                    "round": 1,
                    "participants": [
                        {"id": 51574, "score": 0},
                        {"id": 51592, "score": -1},
                    ],
                },
                {
                    "matchId": 3,
                    "winnerUserId": 51590,
                    "mode": "Tournament",
                    "tournamentId": 1,
                    "parentMatchId": 1,
                    "round": 2,
                    "participants": [
                        {"id": 51590, "score": 0},
                        {"id": 36858, "score": -1},
                    ],
                },
            ],
            "current_round": 4,
            "state": "finished",
        },
    ]
    return mocker.patch(
        "tournament_app.utils.tournament_session.TournamentSession.update_matches_data",
        side_effect=dummy_matches_data_list,
    )


@pytest.fixture
def mock_fetch_matches_data(mocker):
    """
    fetch_matches_data１回目の呼び出しは正常、2回目の呼び出しはエラーとなるようにモック
    """
    mock_response1 = MagicMock(spec=requests.Response)
    mock_response1.status_code = 200
    mock_response1.json.return_value = {
        "results": [
            {
                "matchId": 1,
                "winnerUserId": None,
                "mode": "Tournament",
                "tournamentId": 1,
                "parentMatchId": None,
                "round": 3,
                "participants": [],
            },
            {
                "matchId": 2,
                "winnerUserId": None,
                "mode": "Tournament",
                "tournamentId": 1,
                "parentMatchId": 1,
                "round": 1,
                "participants": [
                    {"id": 51574, "score": None},
                    {"id": 51592, "score": None},
                ],
            },
            {
                "matchId": 3,
                "winnerUserId": None,
                "mode": "Tournament",
                "tournamentId": 1,
                "parentMatchId": 1,
                "round": 2,
                "participants": [
                    {"id": 51590, "score": None},
                    {"id": 36858, "score": None},
                ],
            },
        ],
        "current_round": 1,
        "state": "ongoing",
    }

    mock_response2 = MagicMock(spec=requests.Response)
    mock_response2.status_code = 500
    mocker.patch(
        "tournament_app.utils.match_client.MatchClient.fetch_matches_data",
        side_effect=[mock_response1, mock_response2],
    )


@pytest.fixture()
def mock_limit_tournament_match_sec(mocker):
    """TournamentSession.LIMIT_TOURNAMENT_MATCH_SEC をモックして値を変更"""
    mocker.patch.object(TournamentSession, "LIMIT_TOURNAMENT_MATCH_SEC", 1)


@pytest.fixture
def mock_handle_tournament_match_bye():
    """
    TaskTimerで実行されるhandle_tournament_match_byeをupdate_tournament_session_infoに置き換える

    [INFO] diff(update_tournament_session_info, handle_tournament_match_bye) => matches/finishを叩く処理
    """
    with patch.object(
        TournamentSession,
        "handle_tournament_match_bye",
        new=TournamentSession.update_tournament_session_info,
    ):
        yield
