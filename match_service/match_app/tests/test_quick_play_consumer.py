from datetime import timedelta

import jwt
import pytest
from channels.db import database_sync_to_async
from channels.testing import WebsocketCommunicator
from config.asgi import application

from match_app.consumers.quick_play_consumer import QuickPlayConsumer
from match_app.models import MatchParticipant
from match_app.utils.quick_play_matching_manager import QuickPlayMatchingManager

PATH_MATCHING = "/matches/ws/enter-room"


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


async def create_communicator(user_id: int):
    """JWTをCookieに含んでWebSocketコネクションを作成"""
    access_token = create_jwt_for_user(user_id)
    communicator = WebsocketCommunicator(application, PATH_MATCHING)
    communicator.scope["cookies"] = {"access_token": access_token}
    connected, _ = await communicator.connect()
    return communicator, connected


@database_sync_to_async
def check_match_participant_exist(user_id: int) -> bool:
    return MatchParticipant.objects.filter(user_id=user_id).exists()


@pytest.mark.asyncio(loop_scope="function")
@pytest.mark.django_db
async def test_fetch_games_success(mock_fetch_games_success):
    """正常にQuickPlayのマッチングが完了"""
    comms = []
    for i in range(QuickPlayConsumer.ROOM_CAPACITY):
        user_id = i + 1
        communicator, _ = await create_communicator(user_id)
        comms.append(communicator)

    for communicator in comms:
        res = await communicator.receive_json_from()
        assert res.get("match_id", None) is not None
        assert res["match_id"] != "None"
        expect_user_id_list = [
            str(i + 1) for i in range(QuickPlayConsumer.ROOM_CAPACITY)
        ]
        assert res["user_id_list"] == expect_user_id_list

    [await communicator.disconnect() for communicator in comms]
    QuickPlayMatchingManager.clear_waiting_users()


@pytest.mark.asyncio(loop_scope="function")
@pytest.mark.django_db
async def test_featch_games_error(mock_fetch_games_error):
    """
    gamesエンドポイントを叩く処理が失敗した場合、match_id = "None"が返る
    失敗した場合、試合レコードと試合参加者レコードは作成されない
    """
    comms = []
    user_ids = [(i + 10) for i in range(QuickPlayConsumer.ROOM_CAPACITY)]
    for user_id in user_ids:
        communicator, _ = await create_communicator(user_id)
        comms.append(communicator)

    for communicator in comms:
        res = await communicator.receive_json_from()
        assert res.get("match_id", None) is not None
        assert res["match_id"] == "None"

    for user_id in user_ids:
        #  試合参加者レコードが存在しないことを確認(rollbackされているか)
        is_exist = await check_match_participant_exist(user_id)
        assert not is_exist

    [await communicator.disconnect() for communicator in comms]
    QuickPlayMatchingManager.clear_waiting_users()


@pytest.mark.asyncio(loop_scope="function")
@pytest.mark.django_db
async def test_user_exit_case(mock_fetch_games_success):
    """ルームに入ったUserが退出し、別Usersがマッチングするケース"""
    first_time_user_id = 123
    communicator, _ = await create_communicator(first_time_user_id)
    await communicator.disconnect()

    comms = []
    for i in range(QuickPlayConsumer.ROOM_CAPACITY):
        user_id = i + 1
        communicator, _ = await create_communicator(user_id)
        comms.append(communicator)

    for communicator in comms:
        res = await communicator.receive_json_from()
        assert res.get("match_id", None) is not None
        assert res["match_id"] != "None"
        expect_user_id_list = [
            str(i + 1) for i in range(QuickPlayConsumer.ROOM_CAPACITY)
        ]
        assert res["user_id_list"] == expect_user_id_list

    [await communicator.disconnect() for communicator in comms]
    QuickPlayMatchingManager.clear_waiting_users()


@pytest.mark.asyncio(loop_scope="function")
@pytest.mark.django_db
async def test_fetch_games_success_2_groups(mock_fetch_games_success):
    """２グループマッチングを行う"""
    comms = []
    for i in range(QuickPlayConsumer.ROOM_CAPACITY):
        user_id = i + 1
        communicator, _ = await create_communicator(user_id)
        comms.append(communicator)

    for communicator in comms:
        res = await communicator.receive_json_from()
        assert res.get("match_id", None) is not None
        assert res["match_id"] != "None"
        expect_user_id_list = [
            str(i + 1) for i in range(QuickPlayConsumer.ROOM_CAPACITY)
        ]
        assert res["user_id_list"] == expect_user_id_list

    comms2 = []
    for i in range(QuickPlayConsumer.ROOM_CAPACITY):
        user_id = i + 1
        communicator, _ = await create_communicator(user_id)
        comms2.append(communicator)

    for communicator in comms2:
        res = await communicator.receive_json_from()
        assert res.get("match_id", None) is not None
        assert res["match_id"] != "None"
        expect_user_id_list = [
            str(i + 1) for i in range(QuickPlayConsumer.ROOM_CAPACITY)
        ]
        assert res["user_id_list"] == expect_user_id_list

    [await communicator.disconnect() for communicator in comms]
    [await communicator.disconnect() for communicator in comms2]
    QuickPlayMatchingManager.clear_waiting_users()


@pytest.mark.asyncio(loop_scope="function")
async def test_has_not_jwt():
    """コネクション確立時にJWTを含まないケースはコネクションが確立できない"""
    communicator = WebsocketCommunicator(application, PATH_MATCHING)
    connected, _ = await communicator.connect()
    assert not connected
    QuickPlayMatchingManager.clear_waiting_users()


@pytest.mark.asyncio(loop_scope="function")
async def test_enter_room_same_user():
    """同一ユーザーがマッチングルームに入った場合、コネクションが確立できない"""
    user_id = 1

    communicator1, connected1 = await create_communicator(user_id)
    assert connected1
    _, connected2 = await create_communicator(user_id)
    assert not connected2

    await communicator1.disconnect()
    QuickPlayMatchingManager.clear_waiting_users()
