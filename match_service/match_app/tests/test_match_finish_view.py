from unittest.mock import MagicMock

import pytest
import requests
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from match_app.models import Matches, MatchParticipants

from .set_up_utils import (
    insert_match_participants_record,
    insert_quick_play_record,
    insert_tournament_record,
)


@pytest.fixture()
def requests_post_mocker(mocker):
    mock_response = MagicMock(spec=requests.Response)
    mock_response.status_code = 200
    mock_response.json.return_value = {"message": "Match ended normally"}
    return mocker.patch("requests.post", return_value=mock_response)


def request_match_finish(client, status, match_id, results) -> dict:
    """
    RequestBodyを作成し/matches/finish/エンドポイントを叩く
    正常系レスポンスならMatchesとMatchParticipantsレコードが作成されているかを確認
    """
    data = {"matchId": match_id, "results": results}
    response = client.post(
        "/matches/finish/", data=data, content_type="application/json"
    )
    assert response.status_code == status

    if response.status_code == HTTP_200_OK:
        match = Matches.objects.filter(match_id=match_id).first()
        # トーナメント終了時、finish_dateは必ずセットされる
        assert match.finish_date is not None

        participants = MatchParticipants.objects.filter(match_id=match)
        user_ids = [result["userId"] for result in results]
        for participant in participants:
            user_id = participant.user_id
            # RequestBodyに含まれるuserIdでMatchParticipantsレコードが作成されたか
            assert user_id in user_ids
            score = [
                result["score"] for result in results if result["userId"] == user_id
            ][0]
            # RequestBodyに含まれるscoreでMatchParticipantsレコードが作成されたか
            assert participant.score == score

    return response.json()


def __insert_quick_play_match(user_ids: list[int]) -> int:
    """Matchesレコードを1つ作成し、user_ids分のMatchParticipantsレコードを作成"""
    match = insert_quick_play_record(None)
    match_id = match.match_id
    [insert_match_participants_record(match, user_id) for user_id in user_ids]
    return match_id


def __insert_tournament_match(user_ids: list[int]):
    """Matchesレコードを1つ作成し、user_ids分のMatchParticipantsレコードを作成"""
    match = insert_tournament_record(None, 1, None, 1)
    match_id = match.match_id
    [insert_match_participants_record(match, user_id) for user_id in user_ids]
    return match_id


@pytest.mark.django_db
def test_simple_quick_play_match_finish(client):
    """QuickPlayモードの試合が終了"""
    results = [{"userId": 1, "score": 11}, {"userId": 2, "score": 1}]
    user_ids = [result["userId"] for result in results]
    match_id = __insert_quick_play_match(user_ids)
    res_data = request_match_finish(client, HTTP_200_OK, match_id, results)
    assert res_data.get("finishDate", None) is not None


@pytest.mark.django_db
def test_simple_tournament_match_finish(requests_post_mocker, client):
    """Tournamentモードの試合が終了"""

    results = [{"userId": 1, "score": 11}, {"userId": 2, "score": 1}]
    user_ids = [result["userId"] for result in results]
    match_id = __insert_tournament_match(user_ids)
    res_data = request_match_finish(client, HTTP_200_OK, match_id, results)
    assert res_data.get("finishDate", None) is not None


@pytest.mark.django_db
def test_not_exist_match(client):
    """レコードが存在しない試合"""
    not_exist_match_id = 12345
    results = [{"userId": 1, "score": 11}, {"userId": 2, "score": 1}]
    request_match_finish(client, HTTP_400_BAD_REQUEST, not_exist_match_id, results)


@pytest.mark.django_db
def test_match_id_is_null(client):
    """match_idがnull"""
    match_id = None
    results = [{"userId": 1, "score": 11}, {"userId": 2, "score": 1}]
    request_match_finish(client, HTTP_400_BAD_REQUEST, match_id, results)


@pytest.mark.django_db
def test_few_results_in_request_body(client):
    """results内の試合参加者が少ない"""
    results = [
        {"userId": 1, "score": 11},
        {"userId": 2, "score": 1},
        {"userId": 3, "score": 3},
    ]
    user_ids = [result["userId"] for result in results]
    match_id = __insert_quick_play_match(user_ids)
    # レコード作成後に、RequestBodyで渡すresultsのレコードを削除
    del results[0]
    request_match_finish(client, HTTP_400_BAD_REQUEST, match_id, results)


@pytest.mark.django_db
def test_many_results_in_request_body(client):
    """results内の試合参加者が多い"""
    results = [
        {"userId": 1, "score": 11},
        {"userId": 2, "score": 1},
        {"userId": 3, "score": 3},
    ]
    user_ids = [result["userId"] for result in results]
    match_id = __insert_quick_play_match(user_ids)
    # レコード作成後に、RequestBodyで渡すresultsにレコードを追加
    results.append({"userId": 4, "score": 8})
    request_match_finish(client, HTTP_400_BAD_REQUEST, match_id, results)


@pytest.mark.django_db
def test_unauthorized_user_id(client):
    """試合参加者ではないユーザーがresults内に存在する"""
    results = [
        {"userId": 1, "score": 11},
        {"userId": 2, "score": 1},
    ]
    user_ids = [result["userId"] for result in results]
    match_id = __insert_quick_play_match(user_ids)
    # レコード作成後に、RequestBodyで渡すresultsのuserIdを変更
    results[0]["userId"] = 100
    request_match_finish(client, HTTP_400_BAD_REQUEST, match_id, results)


@pytest.mark.django_db
def test_invalid_user_id(client):
    """user_idがマイナス"""
    results = [
        {"userId": 1, "score": 11},
        {"userId": 2, "score": 1},
    ]
    user_ids = [result["userId"] for result in results]
    match_id = __insert_quick_play_match(user_ids)
    # レコード作成後に、RequestBodyで渡すresultsのuserIdを不正な値に変更
    results[0]["userId"] = -1
    request_match_finish(client, HTTP_400_BAD_REQUEST, match_id, results)


@pytest.mark.django_db
def test_invalid_score(client):
    """scoreがマイナス"""
    results = [
        {"userId": 1, "score": 11},
        {"userId": 2, "score": 1},
    ]
    user_ids = [result["userId"] for result in results]
    match_id = __insert_quick_play_match(user_ids)
    # レコード作成後に、RequestBodyで渡すresultsのscoreを不正な値に変更
    results[0]["score"] = -1
    request_match_finish(client, HTTP_400_BAD_REQUEST, match_id, results)


@pytest.mark.django_db
def test_empty_results(client):
    """resultsが空のリスト"""
    results = [
        {"userId": 1, "score": 11},
        {"userId": 2, "score": 1},
    ]
    user_ids = [result["userId"] for result in results]
    match_id = __insert_quick_play_match(user_ids)
    results = []
    request_match_finish(client, HTTP_400_BAD_REQUEST, match_id, results)


@pytest.mark.django_db
def test_empty_result(client):
    """resultが空のディクト"""
    results = [
        {"userId": 1, "score": 11},
        {"userId": 2, "score": 1},
    ]
    user_ids = [result["userId"] for result in results]
    match_id = __insert_quick_play_match(user_ids)
    results[0] = {}
    request_match_finish(client, HTTP_400_BAD_REQUEST, match_id, results)


@pytest.mark.django_db
def test_results_is_null(client):
    """resultsがnull"""
    results = [
        {"userId": 1, "score": 11},
        {"userId": 2, "score": 1},
    ]
    user_ids = [result["userId"] for result in results]
    match_id = __insert_quick_play_match(user_ids)
    results = None
    request_match_finish(client, HTTP_400_BAD_REQUEST, match_id, results)


@pytest.mark.django_db
def test_multiple_winner(client):
    """勝者が複数いる(最大のscoreが複数存在)"""
    results = [
        {"userId": 1, "score": 11},
        {"userId": 2, "score": 11},
    ]
    user_ids = [result["userId"] for result in results]
    match_id = __insert_quick_play_match(user_ids)
    request_match_finish(client, HTTP_400_BAD_REQUEST, match_id, results)


@pytest.mark.django_db
def test_score_is_zero(client):
    """score is zero(同点では終わらない)"""
    results = [
        {"userId": 1, "score": 0},
        {"userId": 2, "score": 0},
    ]
    user_ids = [result["userId"] for result in results]
    match_id = __insert_quick_play_match(user_ids)
    request_match_finish(client, HTTP_400_BAD_REQUEST, match_id, results)


@pytest.mark.django_db
def test_multiple_user_id(client):
    """１つの試合に同じユーザー参加してはいけない"""
    results = [
        {"userId": 1, "score": 0},
        {"userId": 1, "score": 11},
    ]
    match_id = __insert_quick_play_match([1])
    request_match_finish(client, HTTP_400_BAD_REQUEST, match_id, results)


@pytest.mark.django_db
def test_already_finished(client):
    """試合は既に終了処理されている"""
    results = [
        {"userId": 1, "score": 0},
        {"userId": 2, "score": 11},
    ]
    user_ids = [result["userId"] for result in results]
    match_id = __insert_quick_play_match(user_ids)
    request_match_finish(client, HTTP_200_OK, match_id, results)
    # ２回目のfinish処理は不正
    request_match_finish(client, HTTP_400_BAD_REQUEST, match_id, results)
