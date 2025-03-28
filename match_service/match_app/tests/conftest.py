from unittest.mock import MagicMock

import pytest
import requests

from match_app.models import Match
from match_app.utils.tournament_match_waiter import TournamentMatchWaiter

from .set_up_utils import (
    insert_match_participants_record,
    insert_quick_play_record,
    insert_tournament_record,
)


@pytest.fixture
def set_up_records() -> dict[str, Match]:
    """
    WARN SetUp時により多くのレコードをinsertしてテストしたい場合、
         別のSetUp関数を作成してください
         このSetUp関数の変更は多数のテストに影響する可能性があります
    """
    match_id_dict = (
        __insert_finished_quick_play()
        | __insert_not_finished_quick_play()
        | __insert_not_finished_tournament()
        | __insert_finished_tournament()
        | __insert_only_one_round_finished_tournament()
    )

    return match_id_dict


def __insert_finished_quick_play() -> dict[str, Match]:
    """試合が終了しているQuickPlay"""
    match1 = insert_quick_play_record(winner_user_id=3)
    insert_match_participants_record(match_id=match1, user_id=3, score=11)
    insert_match_participants_record(match_id=match1, user_id=4, score=5)
    return {"match1": match1}


def __insert_not_finished_quick_play() -> dict[str, Match]:
    """試合が終了していないQuickPlay"""
    match2 = insert_quick_play_record(winner_user_id=None)
    insert_match_participants_record(match_id=match2, user_id=1)
    insert_match_participants_record(match_id=match2, user_id=2)
    return {"match2": match2}


def __insert_not_finished_tournament() -> dict[str, Match]:
    """終了していない４人の参加者がいるトーナメント"""
    tournament_id = 1
    match3 = insert_tournament_record(
        winner_user_id=None, tournament_id=tournament_id, parent_match_id=None, round=3
    )

    match4 = insert_tournament_record(
        winner_user_id=None,
        tournament_id=tournament_id,
        parent_match_id=match3,
        round=2,
    )
    insert_match_participants_record(match_id=match4, user_id=3, score=None)
    insert_match_participants_record(match_id=match4, user_id=4, score=None)

    match5 = insert_tournament_record(
        winner_user_id=None,
        tournament_id=tournament_id,
        parent_match_id=match3,
        round=1,
    )
    insert_match_participants_record(match_id=match5, user_id=1, score=None)
    insert_match_participants_record(match_id=match5, user_id=2, score=None)
    return {"match3": match3, "match4": match4, "match5": match5}


def __insert_finished_tournament() -> dict[str, Match]:
    """終了済みの2人の参加者がいるトーナメント"""
    tournament_id = 2
    match6 = insert_tournament_record(
        winner_user_id=1, tournament_id=tournament_id, parent_match_id=None, round=1
    )
    insert_match_participants_record(match_id=match6, user_id=1, score=11)
    insert_match_participants_record(match_id=match6, user_id=2, score=0)
    return {"match6": match6}


def __insert_only_one_round_finished_tournament() -> dict[str, Match]:
    """1ラウンドだけ終了済みの３人の参加者がいるトーナメント"""
    tournament_id = 3
    match7 = insert_tournament_record(
        winner_user_id=None, tournament_id=tournament_id, parent_match_id=None, round=2
    )
    insert_match_participants_record(match_id=match7, user_id=1, score=None)
    insert_match_participants_record(match_id=match7, user_id=3, score=None)

    match8 = insert_tournament_record(
        winner_user_id=1, tournament_id=tournament_id, parent_match_id=match7, round=1
    )
    insert_match_participants_record(match_id=match8, user_id=1, score=11)
    insert_match_participants_record(match_id=match8, user_id=2, score=0)
    return {"match7": match7, "match8": match8}


@pytest.fixture
def mock_fetch_games_success(mocker):
    """
    /gamesエンドポイントを叩く処理(成功)をモック
    """

    return mocker.patch(
        "match_app.client.game_client.GameClient.fetch_games",
        return_value={"message": "Game room created."},
    )


@pytest.fixture
def mock_fetch_games_error(mocker):
    """
    /gamesエンドポイントを叩く処理(失敗)をモック
    """

    return mocker.patch(
        "match_app.client.game_client.GameClient.fetch_games",
        return_value={"error": "Invalid params provided for game room creation."},
    )


@pytest.fixture()
def request_finish_match_success_mocker(mocker):
    """モック対象の処理は正常処理時にResponseを返すため、Responseをモックする"""
    mock_response = MagicMock(spec=requests.Response)
    mock_response.status_code = 200
    mock_response.json.return_value = {"message": "Match ended normally"}
    return mocker.patch(
        "match_app.client.tournament_client.TournamentClient.finish_match",
        return_value=mock_response,
    )


@pytest.fixture()
def request_finish_match_error_mocker(mocker):
    """モック対象の処理はエラー時に500を投げるため、500の発生をモックする"""
    mock_response = MagicMock(spec=requests.Response)
    mock_response.status_code = 500
    mock_response.json.return_value = {"error": "Internal Server Error"}
    return mocker.patch(
        "match_app.client.tournament_client.TournamentClient.finish_match",
        return_value=mock_response,
    )


@pytest.fixture()
def mock_limit_wait_sec(mocker):
    """TournamentMatchWaiter.LIMIT_WAIT_SEC をモックして値を変更"""
    mocker.patch.object(TournamentMatchWaiter, "LIMIT_WAIT_SEC", 1)
