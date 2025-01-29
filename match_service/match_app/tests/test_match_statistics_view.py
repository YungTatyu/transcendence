import pytest

from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from .set_up_records import set_up_records


def request_match_statistics(client, status, user_id) -> dict:
    response = client.get(f"/matches/statistics/{user_id}/")
    assert response.status_code == status
    return response.json()


@pytest.mark.django_db
def test_user1(client, set_up_records):
    user1_id = 1
    res_data = request_match_statistics(client, HTTP_200_OK, user1_id)
    expect_data = {
        "matchWinCount": 2,
        "matchLoseCount": 0,
        "tournamentWinnerCount": 1,
    }
    assert res_data == expect_data


@pytest.mark.django_db
def test_user2(client, set_up_records):
    user2_id = 2
    res_data = request_match_statistics(client, HTTP_200_OK, user2_id)
    expect_data = {
        "matchWinCount": 0,
        "matchLoseCount": 2,
        "tournamentWinnerCount": 0,
    }
    assert res_data == expect_data


@pytest.mark.django_db
def test_user3(client, set_up_records):
    user3_id = 3
    res_data = request_match_statistics(client, HTTP_200_OK, user3_id)
    expect_data = {
        "matchWinCount": 1,
        "matchLoseCount": 0,
        "tournamentWinnerCount": 0,
    }
    assert res_data == expect_data


@pytest.mark.django_db
def test_user4(client, set_up_records):
    user4_id = 4
    res_data = request_match_statistics(client, HTTP_200_OK, user4_id)
    expect_data = {
        "matchWinCount": 0,
        "matchLoseCount": 1,
        "tournamentWinnerCount": 0,
    }
    assert res_data == expect_data


@pytest.mark.django_db
def test_user_not_exist(client, set_up_records):
    """存在しないユーザーでも正常にレスポンスが返る"""
    not_exist_user_id = 12345
    res_data = request_match_statistics(client, HTTP_200_OK, not_exist_user_id)
    expect_data = {
        "matchWinCount": 0,
        "matchLoseCount": 0,
        "tournamentWinnerCount": 0,
    }
    assert res_data == expect_data


@pytest.mark.django_db
def test_user_id_is_not_digit(client, set_up_records):
    """URLのPathのuser_idが数値でないなら400が返る"""
    not_digit_user_id = "abcde"
    request_match_statistics(client, HTTP_400_BAD_REQUEST, not_digit_user_id)
