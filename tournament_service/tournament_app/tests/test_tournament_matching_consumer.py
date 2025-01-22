import pytest
import time
from channels.testing import WebsocketCommunicator
from tournament_app.consumers import TournamentMatchingConsumer as TMC

PATH = "/tournament/ws/enter-room"


class CustomWebsocketCommunicator(WebsocketCommunicator):
    def __init__(self, application, path, scope_override=None):
        super().__init__(application, path)
        if scope_override:
            self.scope.update(scope_override)


async def create_communicator(port: int):
    communicator = CustomWebsocketCommunicator(
        TMC.as_asgi(),
        PATH,
        scope_override={"client": ("127.0.0.1", port)},
    )
    connected, _ = await communicator.connect()
    assert connected
    return communicator


@pytest.mark.asyncio
async def test_enter_room_from_empty_with_one_user():
    """0 -> 1人時は{'tournament_start_time': 'None'}がSendされる"""
    communicator = await create_communicator(10000)
    act_data = await communicator.receive_json_from()
    assert act_data["tournament_start_time"] == "None"
    await communicator.disconnect()


@pytest.mark.asyncio
async def test_enter_room_with_second_user():
    """
    1 -> 2人時はマッチング待機中の全員に
    トーナメント開始UNIX時刻(1->2人になった時刻+FORCED_START_TIME)がSendされる
    """
    communicator1 = await create_communicator(10001)
    await communicator1.receive_json_from()
    communicator2 = await create_communicator(10002)

    data1 = await communicator1.receive_json_from()
    data2 = await communicator2.receive_json_from()
    start_time1 = float(data1["tournament_start_time"])
    start_time2 = float(data2["tournament_start_time"])
    now = time.time()
    assert now <= start_time1 <= (now + TMC.FORCED_START_TIME)
    assert now <= start_time2 <= (now + TMC.FORCED_START_TIME)

    await communicator1.disconnect()
    await communicator2.disconnect()


@pytest.mark.asyncio
async def test_exit_room_with_two_users():
    """2 -> 1人時は{'tournament_start_time': 'None'}がSendされる"""
    communicator1 = await create_communicator(10001)
    await communicator1.receive_json_from()

    communicator2 = await create_communicator(10002)
    await communicator1.receive_json_from()
    await communicator2.receive_json_from()

    await communicator2.disconnect()
    data = await communicator1.receive_json_from()
    assert data["tournament_start_time"] == "None"

    await communicator1.disconnect()


# INFO @pytest.mark.django_dbはアプリケーション内で実際にDB操作を行うテストに付与しないとエラー
# INFO @pytest.mark.django_dbを付与したテストで作成されたレコードはテスト後にロールバックされ、永続化しない。
@pytest.mark.asyncio
@pytest.mark.django_db
async def test_start_tournament_by_room_capacity():
    """ROOM_CAPACITYに達した時にtournament_idが送信されるか"""
    communicators = []
    for i in range(TMC.ROOM_CAPACITY):
        communicators.append(await create_communicator(1000 + i))
        # tournament_start_timeの通知はWebSocketが作成されるたびにルーム内の全員にSendされる
        [await communicator.receive_json_from() for communicator in communicators]

    for communicator in communicators:
        data = await communicator.receive_json_from()
        assert data == {"tournament_id": "1"}

    for communicator in communicators:
        await communicator.disconnect()
