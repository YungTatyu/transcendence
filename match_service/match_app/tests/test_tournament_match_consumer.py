from datetime import timedelta

import jwt
import pytest
from channels.db import database_sync_to_async
from channels.testing import WebsocketCommunicator
from config.asgi import application

from match_app.consumers.tournament_match_consumer import TournamentMatchWaiter
from match_app.models import Match, MatchParticipant

PATH_WAITING_FORMAT = "/matches/ws/enter-room/{}"


def create_jwt_for_user(user_id):
    # JWTを生成するロジック
    payload = {
        "user_id": user_id,
        "exp": timedelta(days=1).total_seconds(),
        "iat": timedelta(days=0).total_seconds(),
    }
    secret_key = "your_secret_key"
    token = jwt.encode(payload, secret_key, algorithm="HS256")
    return token


async def create_communicator(user_id: int, match_id: int, expect_connected=True):
    """JWTをCookieに含んでWebSocketコネクションを作成"""
    access_token = create_jwt_for_user(user_id)
    communicator = WebsocketCommunicator(
        application, PATH_WAITING_FORMAT.format(match_id)
    )
    communicator.scope["cookies"] = {"access_token": access_token}
    connected, _ = await communicator.connect()
    assert connected == expect_connected
    return communicator


@database_sync_to_async
def insert_tournament_match(
    user_id_list, mode="Tournament", tournament_id=123456, parent_match=None, round=1
) -> Match:
    tournament_match = Match.objects.create(
        mode=mode,
        tournament_id=tournament_id,
        parent_match_id=parent_match,
        round=round,
    )

    for user_id in user_id_list:
        MatchParticipant.objects.create(match_id=tournament_match, user_id=user_id)
    return tournament_match


@pytest.mark.asyncio(loop_scope="function")
@pytest.mark.django_db
async def test_start_tournment_match():
    """正常にトーナメントの試合が開始されるケース"""
    user_id_list = [1, 2]
    match = await insert_tournament_match(user_id_list)

    comms = []
    for user_id in user_id_list:
        communicator = await create_communicator(user_id, match.match_id)
        comms.append(communicator)

    for communicator in comms:
        res = await communicator.receive_json_from()
        assert res.get("match_id", None) is not None
        assert res["match_id"] != "None"
        expect_user_id_list = [str(user_id) for user_id in user_id_list]
        assert sorted(res["user_id_list"]) == sorted(expect_user_id_list)

    [await communicator.disconnect() for communicator in comms]
    TournamentMatchWaiter.clear()


@pytest.mark.asyncio(loop_scope="function")
@pytest.mark.django_db
async def test_not_exist_match_id():
    """存在しないmatch_idのURLでコネクションを確立しようとしたケース"""
    user_id = 1
    not_exist_match_id = 123
    await create_communicator(user_id, not_exist_match_id, expect_connected=False)
    TournamentMatchWaiter.clear()


@pytest.mark.asyncio(loop_scope="function")
@pytest.mark.django_db
async def test_invalid_mode():
    """modeがTournamentモード出ないケース"""
    user_id_list = [1, 2]
    match = await insert_tournament_match(user_id_list, mode="QuickPlay")
    await create_communicator(user_id_list[0], match.match_id, expect_connected=False)
    TournamentMatchWaiter.clear()


@pytest.mark.asyncio(loop_scope="function")
@pytest.mark.django_db
async def test_prev_round_has_not_been_completed():
    """一つ前のラウンドが終了していないケース"""
    round1_user_id_list = [1, 2]
    round2_user_id_list = [3, 4]
    match1 = await insert_tournament_match(round1_user_id_list)
    match2 = await insert_tournament_match(round2_user_id_list, parent_match=match1)

    # １ラウンド目なのでregister可能
    communicator = await create_communicator(round1_user_id_list[0], match1.match_id)
    # １ラウンド目が終了していないため、２ラウンド目はregister不可能
    await create_communicator(round2_user_id_list[0], match2.match_id)

    await communicator.disconnect()
    TournamentMatchWaiter.clear()


@pytest.mark.asyncio(loop_scope="function")
@pytest.mark.django_db
async def test_no_register_user_id():
    """試合参加者でないユーザーが試合に参加しようとするケース"""
    user_id_list = [1, 2]
    no_register_user_id = 3
    match = await insert_tournament_match(user_id_list)
    communicator = await create_communicator(
        no_register_user_id, match.match_id, expect_connected=False
    )
    await communicator.disconnect()
    TournamentMatchWaiter.clear()
