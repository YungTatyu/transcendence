from datetime import timedelta

import jwt
import pytest
from channels.testing import WebsocketCommunicator
from config.asgi import application
from match_app.utils.quick_play_matching_manager import QuickPlayMatchingManager
from match_app.consumers.quick_play_consumer import QuickPlayConsumer

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


async def create_communicator(user_id: int, expect_connected=True):
    """JWTをCookieに含んでWebSocketコネクションを作成"""
    access_token = create_jwt_for_user(user_id)
    communicator = WebsocketCommunicator(application, PATH_MATCHING)
    communicator.scope["cookies"] = {"access_token": access_token}
    connected, _ = await communicator.connect()
    assert connected == expect_connected
    return communicator


@pytest.mark.asyncio(loop_scope="function")
@pytest.mark.django_db
async def test_fetch_games_success(mock_fetch_games_success):
    """正常にQuickPlayのマッチングが完了"""
    comms = []
    for i in range(QuickPlayConsumer.ROOM_CAPACITY):
        user_id = i + 1
        communicator = await create_communicator(user_id)
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
    """gamesエンドポイントを叩く処理が失敗した場合、match_id = "None"が返る"""
    comms = []
    for i in range(QuickPlayConsumer.ROOM_CAPACITY):
        user_id = i + 1
        communicator = await create_communicator(user_id)
        comms.append(communicator)

    for communicator in comms:
        res = await communicator.receive_json_from()
        assert res.get("match_id", None) is not None
        assert res["match_id"] == "None"

    [await communicator.disconnect() for communicator in comms]
    QuickPlayMatchingManager.clear_waiting_users()


@pytest.mark.asyncio(loop_scope="function")
@pytest.mark.django_db
async def test_user_exit_case(mock_fetch_games_success):
    """ルームに入ったUserが退出し、別Usersがマッチングするケース"""
    first_time_user_id = 123
    communicator = await create_communicator(first_time_user_id)
    await communicator.disconnect()

    comms = []
    for i in range(QuickPlayConsumer.ROOM_CAPACITY):
        user_id = i + 1
        communicator = await create_communicator(user_id)
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
        communicator = await create_communicator(user_id)
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
        communicator = await create_communicator(user_id)
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

    communicator = await create_communicator(user_id)
    await create_communicator(user_id, expect_connected=False)
    await communicator.disconnect()
    QuickPlayMatchingManager.clear_waiting_users()
