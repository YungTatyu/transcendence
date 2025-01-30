import pytest
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from match_app.models import Matches, MatchParticipants


def request_tournament_match(
    client, status, user_id_list, tournament_id, parent_match_id, round
) -> dict:
    data = {
        "userIdList": user_id_list,
        "tournamentId": tournament_id,
        "parentMatchId": parent_match_id,
        "round": round,
    }
    response = client.post(
        f"/matches/tournament-match/", data=data, content_type="application/json"
    )
    assert response.status_code == status

    # StatusCode == 200 -> 正常にレコードが作成されたかを確認
    if response.status_code == HTTP_200_OK:
        match = Matches.objects.filter(tournament_id=tournament_id).first()
        assert match.match_id >= 0  # match_idは0以上の値が自動で採番される
        assert match.winner_user_id is None  # nullがセットされる
        assert match.mode == "Tournament"
        assert match.start_date is not None  # 現在時刻がセットされる
        assert match.finish_date is None  # nullがセットされる
        if parent_match_id is None:
            assert match.parent_match_id is None
        else:
            assert match.parent_match_id.match_id == parent_match_id
        assert match.round == round

        participants = MatchParticipants.objects.filter(match_id=match)
        # RequestBodyのuser_id_listとMatchParticipantsのuser_idのリストが同じか
        assert len(user_id_list) == len(participants)
        for participant in participants:
            assert participant.user_id in user_id_list
            assert participant.score is None  # nullがセットされる

    return response.json()


@pytest.mark.django_db
def test_participants_0(client):
    """トーナメント試合作成時に参加者が決まっていない試合は存在する"""
    participants = []
    res_data = request_tournament_match(client, HTTP_200_OK, participants, 1, None, 1)
    assert res_data.get("matchId", None) is not None


@pytest.mark.django_db
def test_participants_1(client):
    """トーナメント試合作成時、対戦相手が決まっていない試合は存在する"""
    participants = [1]
    request_tournament_match(client, HTTP_200_OK, participants, 1, None, 1)


@pytest.mark.django_db
def test_participants_2(client):
    participants = [1, 2]
    request_tournament_match(client, HTTP_200_OK, participants, 1, None, 1)


@pytest.mark.django_db
def test_participants_3(client):
    """3人以上の参加者がいる試合は作成可能"""
    participants = [1, 2, 3]
    request_tournament_match(client, HTTP_200_OK, participants, 1, None, 1)


@pytest.mark.django_db
def test_have_parent_match(client):
    """親試合を持つ試合を作成"""
    res_data = request_tournament_match(client, HTTP_200_OK, [], 3, None, 3)
    parent_match_id = res_data["matchId"]
    request_tournament_match(client, HTTP_200_OK, [3, 4], 2, parent_match_id, 2)
    request_tournament_match(client, HTTP_200_OK, [1, 2], 1, parent_match_id, 1)


@pytest.mark.django_db
def test_invalid_user_id(client):
    """user_idにマイナス値は許容されない"""
    participants = [1, -1]
    request_tournament_match(client, HTTP_400_BAD_REQUEST, participants, 1, None, 1)


@pytest.mark.django_db
def test_duplicate_user_id(client):
    """user_idが重複"""
    participants = [1, 1]
    request_tournament_match(client, HTTP_400_BAD_REQUEST, participants, 1, None, 1)


@pytest.mark.django_db
def test_user_id_list_is_null(client):
    """user_id_listがnull"""
    participants = None
    request_tournament_match(client, HTTP_400_BAD_REQUEST, participants, 1, None, 1)


@pytest.mark.django_db
def test_user_id_is_null(client):
    """user_idがnull"""
    participants = [1, None]
    request_tournament_match(client, HTTP_400_BAD_REQUEST, participants, 1, None, 1)


@pytest.mark.django_db
def test_invalid_tournament_id(client):
    """tournament_idにマイナス値は許容されない"""
    tournament_id = -1
    request_tournament_match(
        client, HTTP_400_BAD_REQUEST, [1, 2], tournament_id, None, 1
    )


@pytest.mark.django_db
def test_tournament_id_is_null(client):
    """tournament_idがnull"""
    tournament_id = None
    request_tournament_match(
        client, HTTP_400_BAD_REQUEST, [1, 2], tournament_id, None, 1
    )


@pytest.mark.django_db
def test_parent_not_exist(client):
    """parent_idに指定した試合が存在しない"""
    parent_id = 12345
    request_tournament_match(client, HTTP_400_BAD_REQUEST, [1, 2], 1, parent_id, 1)


@pytest.mark.django_db
def test_same_tournament_id_and_round(client):
    """同一のtournament_idとroundを持つ試合は作成不可"""
    tournament_id = 1
    round = 1
    request_tournament_match(client, HTTP_200_OK, [3, 4], tournament_id, None, round)
    request_tournament_match(
        client, HTTP_400_BAD_REQUEST, [1, 2], tournament_id, None, round
    )


@pytest.mark.django_db
def test_invalid_round(client):
    """roundは1以上の数値である必要がある"""
    round = 0
    request_tournament_match(client, HTTP_400_BAD_REQUEST, [1, 2], 1, None, round)


@pytest.mark.django_db
def test_round_is_null(client):
    """roundがnull"""
    round = None
    request_tournament_match(client, HTTP_400_BAD_REQUEST, [1, 2], 1, None, round)
