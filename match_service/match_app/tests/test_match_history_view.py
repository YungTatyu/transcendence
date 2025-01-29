import pytest
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from .set_up_utils import set_up_records, create_query_string


def request_match_histories(client, status, user_id, offset=None, limit=None) -> dict:
    query_string = create_query_string(offset=offset, limit=limit)
    response = client.get(f"/matches/histories/{user_id}/{query_string}")
    assert response.status_code == status
    return response.json()


@pytest.mark.django_db
def test_user1(client, set_up_records):
    user1_id = 1
    res_data = request_match_histories(client, HTTP_200_OK, user1_id)

    assert res_data["total"] == 2
    assert res_data["offset"] == 0
    assert res_data["limit"] == 2

    for result in res_data["results"]:
        assert result["mode"] == "Tournament"
        assert result["result"] == "win"
        assert result["date"] is not None
        assert result["userScore"] == 11
        assert result["opponents"][0] == {"id": 2, "score": 0}


@pytest.mark.django_db
def test_user2(client, set_up_records):
    user2_id = 2
    res_data = request_match_histories(client, HTTP_200_OK, user2_id)

    assert res_data["total"] == 2
    assert res_data["offset"] == 0
    assert res_data["limit"] == 2

    for result in res_data["results"]:
        assert result["mode"] == "Tournament"
        assert result["result"] == "lose"
        assert result["date"] is not None
        assert result["userScore"] == 0
        assert result["opponents"][0] == {"id": 1, "score": 11}


@pytest.mark.django_db
def test_user3(client, set_up_records):
    user3_id = 3
    res_data = request_match_histories(client, HTTP_200_OK, user3_id)

    assert res_data["total"] == 1
    assert res_data["offset"] == 0
    assert res_data["limit"] == 1

    for result in res_data["results"]:
        assert result["mode"] == "QuickPlay"
        assert result["result"] == "win"
        assert result["date"] is not None
        assert result["userScore"] == 11
        assert result["opponents"][0] == {"id": 4, "score": 5}


@pytest.mark.django_db
def test_user4(client, set_up_records):
    user4_id = 4
    res_data = request_match_histories(client, HTTP_200_OK, user4_id)

    assert res_data["total"] == 1
    assert res_data["offset"] == 0
    assert res_data["limit"] == 1

    for result in res_data["results"]:
        assert result["mode"] == "QuickPlay"
        assert result["result"] == "lose"
        assert result["date"] is not None
        assert result["userScore"] == 5
        assert result["opponents"][0] == {"id": 3, "score": 11}


@pytest.mark.django_db
def test_user_not_exist(client, set_up_records):
    """存在しないユーザーでも正常にレスポンスが返る"""
    not_exist_user_id = 12345
    res_data = request_match_histories(client, HTTP_200_OK, not_exist_user_id)

    assert res_data["total"] == 0
    assert res_data["offset"] == 0
    assert res_data["limit"] == 0
    assert res_data["results"] == []


@pytest.mark.django_db
def test_user_id_is_not_digit(client, set_up_records):
    """URLのPathのuser_idが数値でないなら400が返る"""
    not_digit_user_id = "abcde"
    request_match_histories(client, HTTP_400_BAD_REQUEST, not_digit_user_id)


@pytest.mark.django_db
def test_offset(client, set_up_records):
    """
    test_user1に?offset=1を追加
    offsetが1ずれる分、limit(取得できたレコード数)は1減った値となる
    """
    user1_id = 1
    offset = 1
    res_data = request_match_histories(client, HTTP_200_OK, user1_id, offset=offset)
    assert res_data["total"] == 2
    assert res_data["offset"] == 1
    assert res_data["limit"] == 1

    for result in res_data["results"]:
        assert result["mode"] == "Tournament"
        assert result["result"] == "win"
        assert result["date"] is not None
        assert result["userScore"] == 11
        assert result["opponents"][0] == {"id": 2, "score": 0}


@pytest.mark.django_db
def test_limit(client, set_up_records):
    """
    test_user1に?limit=1を追加
    test_user1では2レコード取得できたが、limit=1なので最大でも1件しか取得できない
    """
    user1_id = 1
    limit = 1
    res_data = request_match_histories(client, HTTP_200_OK, user1_id, limit=limit)
    assert res_data["total"] == 2
    assert res_data["offset"] == 0
    assert res_data["limit"] == 1

    result = res_data["results"][0]
    assert result["mode"] == "Tournament"
    assert result["result"] == "win"
    assert result["date"] is not None
    assert result["userScore"] == 11
    assert result["opponents"][0] == {"id": 2, "score": 0}


@pytest.mark.django_db
def test_offset_over_total(client, set_up_records):
    """
    offsetがサーバ内の合計レコード数より大きいケース
    resultsは空のリストが返る
    """
    user1_id = 1
    offset = 3
    res_data = request_match_histories(client, HTTP_200_OK, user1_id, offset=offset)
    assert res_data["total"] == 2
    assert res_data["offset"] == 3
    assert res_data["limit"] == 0
    assert res_data["results"] == []


@pytest.mark.django_db
def test_limit_over_total(client, set_up_records):
    """
    limitがサーバ内の合計レコード数より大きいケース
    レスポンスボディのlimitは
    QueryStringで指定したlimitに関係なく、取得できたレコード数が返る
    """
    user1_id = 1
    limit = 3
    res_data = request_match_histories(client, HTTP_200_OK, user1_id, limit=limit)
    assert res_data["total"] == 2
    assert res_data["offset"] == 0
    assert res_data["limit"] == 2

    for result in res_data["results"]:
        assert result["mode"] == "Tournament"
        assert result["result"] == "win"
        assert result["date"] is not None
        assert result["userScore"] == 11
        assert result["opponents"][0] == {"id": 2, "score": 0}


@pytest.mark.django_db
def test_offset_and_limit(client, set_up_records):
    """
    offsetとlimitのどちらも指定するケース
    """
    user1_id = 1
    offset = 1
    limit = 1
    res_data = request_match_histories(
        client, HTTP_200_OK, user1_id, offset=offset, limit=limit
    )
    assert res_data["total"] == 2
    assert res_data["offset"] == 1
    assert res_data["limit"] == 1

    result = res_data["results"][0]
    assert result["mode"] == "Tournament"
    assert result["result"] == "win"
    assert result["date"] is not None
    assert result["userScore"] == 11
    assert result["opponents"][0] == {"id": 2, "score": 0}


@pytest.mark.django_db
def test_offset_and_limit_over_total(client, set_up_records):
    """
    offsetとlimitのどちらも指定
    サーバ内のレコード数よりも大きい値が指定されるケース
    """
    user1_id = 1
    offset = 1
    limit = 10
    res_data = request_match_histories(
        client, HTTP_200_OK, user1_id, offset=offset, limit=limit
    )
    assert res_data["total"] == 2
    assert res_data["offset"] == 1
    assert res_data["limit"] == 1

    result = res_data["results"][0]
    assert result["mode"] == "Tournament"
    assert result["result"] == "win"
    assert result["date"] is not None
    assert result["userScore"] == 11
    assert result["opponents"][0] == {"id": 2, "score": 0}
