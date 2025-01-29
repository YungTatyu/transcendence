import pytest
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from match_app.models import Matches, MatchParticipants
from .set_up_utils import (
    insert_quick_play_record,
    insert_tournament_record,
    insert_match_participants_record,
)


def request_match_finish(client, status, match_id, results) -> dict:
    data = {"matchId": match_id, "results": results}
    response = client.post(
        "/matches/finish/", data=data, content_type="application/json"
    )
    assert response.status_code == status

    if response.status_code == HTTP_200_OK:
        match = Matches.objects.filter(match_id=match_id).first()
        assert match.finish_date is not None

        participants = MatchParticipants.objects.filter(match_id=match)
        user_ids = [result["userId"] for result in results]
        for participant in participants:
            user_id = participant.user_id
            assert user_id in user_ids
            score = [
                result["score"] for result in results if result["userId"] == user_id
            ][0]
            assert participant.score == score

    return response.json()


def insert_quick_play_match(user_ids: list[int]) -> int:
    match = insert_quick_play_record(None)
    match_id = match.match_id
    [insert_match_participants_record(match, user_id) for user_id in user_ids]
    return match_id


def insert_tournament_match(user_ids: list[int]):
    match = insert_tournament_record(None, 1, None, 1)
    match_id = match.match_id
    [insert_match_participants_record(match, user_id) for user_id in user_ids]
    return match_id


@pytest.mark.django_db
def test_simple_quick_play_match_finish(client):
    """QuickPlayモードの試合が終了"""
    results = [{"userId": 1, "score": 11}, {"userId": 2, "score": 1}]
    user_ids = [result["userId"] for result in results]
    match_id = insert_quick_play_match(user_ids)
    res_data = request_match_finish(client, HTTP_200_OK, match_id, results)
    assert res_data.get("finishDate", None) is not None


@pytest.mark.django_db
def test_simple_tournament_match_finish(client):
    """Tournamentモードの試合が終了"""
    results = [{"userId": 1, "score": 11}, {"userId": 2, "score": 1}]
    user_ids = [result["userId"] for result in results]
    match_id = insert_tournament_match(user_ids)
    res_data = request_match_finish(client, HTTP_200_OK, match_id, results)
    assert res_data.get("finishDate", None) is not None


@pytest.mark.django_db
def test_not_exist_match(client):
    """レコードが存在しない試合"""
    results = [{"userId": 1, "score": 11}, {"userId": 2, "score": 1}]
    not_exist_match_id = 12345
    request_match_finish(client, HTTP_400_BAD_REQUEST, not_exist_match_id, results)


@pytest.mark.django_db
def test_match_id_is_null(client):
    """match_idがnull"""
    results = [{"userId": 1, "score": 11}, {"userId": 2, "score": 1}]
    match_id = None
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
    match_id = insert_quick_play_match(user_ids)
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
    match_id = insert_quick_play_match(user_ids)
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
    match_id = insert_quick_play_match(user_ids)
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
    match_id = insert_quick_play_match(user_ids)
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
    match_id = insert_quick_play_match(user_ids)
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
    match_id = insert_quick_play_match(user_ids)
    results = []
    request_match_finish(client, HTTP_400_BAD_REQUEST, match_id, results)


@pytest.mark.django_db
def test_empty_result(client):
    """resultsが空のリスト"""
    results = [
        {"userId": 1, "score": 11},
        {"userId": 2, "score": 1},
    ]
    user_ids = [result["userId"] for result in results]
    match_id = insert_quick_play_match(user_ids)
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
    match_id = insert_quick_play_match(user_ids)
    results = None
    request_match_finish(client, HTTP_400_BAD_REQUEST, match_id, results)


@pytest.mark.django_db
def test_multiple_winner(client):
    """勝者が複数いる"""
    results = [
        {"userId": 1, "score": 11},
        {"userId": 2, "score": 11},
    ]
    user_ids = [result["userId"] for result in results]
    match_id = insert_quick_play_match(user_ids)
    request_match_finish(client, HTTP_400_BAD_REQUEST, match_id, results)


@pytest.mark.django_db
def test_score_is_zero(client):
    """score is zero"""
    results = [
        {"userId": 1, "score": 0},
        {"userId": 2, "score": 0},
    ]
    user_ids = [result["userId"] for result in results]
    match_id = insert_quick_play_match(user_ids)
    request_match_finish(client, HTTP_400_BAD_REQUEST, match_id, results)


@pytest.mark.django_db
def test_multiple_user_id(client):
    """score is zero"""
    results = [
        {"userId": 1, "score": 0},
        {"userId": 1, "score": 11},
    ]
    match_id = insert_quick_play_match([1])
    request_match_finish(client, HTTP_400_BAD_REQUEST, match_id, results)


@pytest.mark.django_db
def test_already_finished(client):
    """試合は既に終了処理されている"""
    results = [
        {"userId": 1, "score": 0},
        {"userId": 2, "score": 11},
    ]
    user_ids = [result["userId"] for result in results]
    match_id = insert_quick_play_match(user_ids)
    request_match_finish(client, HTTP_200_OK, match_id, results)
    request_match_finish(client, HTTP_400_BAD_REQUEST, match_id, results)
