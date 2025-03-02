import asyncio
import time

import pytest
from channels.testing import WebsocketCommunicator

from tournament_app.consumers.tournament_matching_consumer import (
    TournamentMatchingConsumer as Tmc,
)
from tournament_app.utils.tournament_matching_manager import (
    TournamentMatchingManager as Tmm,
)
from tournament_app.utils.tournament_session import TournamentSession

PATH = "/tournament/ws/enter-room"


class CustomWebsocketCommunicator(WebsocketCommunicator):
    def __init__(self, application, path, scope_override=None):
        super().__init__(application, path)
        if scope_override:
            self.scope.update(scope_override)


async def create_communicator(port: int):
    communicator = CustomWebsocketCommunicator(
        Tmc.as_asgi(),
        PATH,
        scope_override={"client": ("127.0.0.1", port)},
    )
    connected, _ = await communicator.connect()
    assert connected
    return communicator


@pytest.mark.asyncio(loop_scope="function")
async def test_enter_room_from_empty_with_one_user():
    """0 -> 1人時は{'tournament_start_time': 'None'}がSendされる"""
    communicator = await create_communicator(10000)
    act_data = await communicator.receive_json_from()
    assert act_data["tournament_start_time"] == "None"
    await communicator.disconnect()


@pytest.mark.asyncio(loop_scope="function")
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
    assert now <= start_time1 <= (now + Tmc.FORCED_START_TIME)
    assert now <= start_time2 <= (now + Tmc.FORCED_START_TIME)

    await communicator1.disconnect()
    await communicator2.disconnect()


@pytest.mark.asyncio(loop_scope="function")
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


@pytest.mark.asyncio(loop_scope="function")
async def test_same_port():
    """
    同じポート番号のWebSocketを拒否するか
    TODO ポート番号 -> userIdを用いたユーザーの識別に変更時、このテストも変更する
    """
    port = 10000
    communicator1 = await create_communicator(port)
    await communicator1.receive_json_from()
    communicator2 = CustomWebsocketCommunicator(
        Tmc.as_asgi(),
        PATH,
        scope_override={"client": ("127.0.0.1", port)},
    )
    connected, _ = await communicator2.connect()
    assert connected is False  # 接続が拒否される

    await communicator1.disconnect()


# INFO @pytest.mark.django_dbはアプリケーション内で実際にDB操作を行うテストに付与しないとエラー
# INFO @pytest.mark.django_dbを付与したテストで作成されたレコードはテスト後にロールバックされ、永続化しない。
@pytest.mark.asyncio(loop_scope="function")
@pytest.mark.django_db
@pytest.mark.usefixtures("update_matches_data_mocker")
async def test_start_tournament_by_room_capacity(create_match_records_mocker):
    """ROOM_CAPACITYに達した時にtournament_idが送信されるか"""
    communicators = []
    for i in range(Tmc.ROOM_CAPACITY):
        communicators.append(await create_communicator(10000 + i))
        # tournament_start_timeの通知はWebSocketが作成されるたびにルーム内の全員にSendされる
        [await communicator.receive_json_from() for communicator in communicators]

    for communicator in communicators:
        data = await communicator.receive_json_from()
        assert "tournament_id" in data

    for communicator in communicators:
        await communicator.disconnect()


@pytest.mark.asyncio(loop_scope="function")
@pytest.mark.django_db
@pytest.mark.usefixtures("update_matches_data_mocker")
async def test_start_tournament_by_force_start_time(create_match_records_mocker):
    """FORCED_START_TIMEに達した時にtournament_idが送信されるか"""
    communicators = []

    # ROOM_CAPACITYに満たない数のWebSocketを作成する
    for i in range(Tmc.ROOM_CAPACITY - 1):
        communicators.append(await create_communicator(10000 + i))
        [await communicator.receive_json_from() for communicator in communicators]

    # FORCED_START_TIME秒以上待機
    await asyncio.sleep(Tmc.FORCED_START_TIME + 1)

    for communicator in communicators:
        data = await communicator.receive_json_from()
        assert "tournament_id" in data

    for communicator in communicators:
        await communicator.disconnect()


@pytest.mark.asyncio(loop_scope="function")
@pytest.mark.django_db
@pytest.mark.usefixtures("update_matches_data_mocker")
async def test_not_start_tournament():
    """FORCED_START_TIMEに達していない場合にtournament_idが送信されないか"""
    communicators = []

    # ROOM_CAPACITYに満たない数のWebSocketを作成する
    for i in range(Tmc.ROOM_CAPACITY - 1):
        communicators.append(await create_communicator(10000 + i))
        [await communicator.receive_json_from() for communicator in communicators]

    # FORCED_START_TIMEに満たない秒数待機
    await asyncio.sleep(Tmc.FORCED_START_TIME - 1)

    for communicator in communicators:
        # サーバから送信されたデータが無いことを確認
        assert await communicator.receive_nothing(timeout=0.1, interval=0.01) is True

    for communicator in communicators:
        await communicator.disconnect()


@pytest.mark.asyncio(loop_scope="function")
@pytest.mark.django_db
@pytest.mark.usefixtures("update_matches_data_mocker")
async def test_init_matching_room_after_start_tournament(create_match_records_mocker):
    """
    トーナメント開始後、マッチングルームが初期化され、別ユーザーがマッチングできるか

    communicators_1 -> 初めにマッチングルームに入り、トーナメントを開始するグループ
    communicators_2 -> communicators_1がトーナメント開始後にマッチングルームに入り、トーナメントを開始するグループ
    """
    communicators_1 = []
    for i in range(Tmc.ROOM_CAPACITY):
        communicators_1.append(await create_communicator(10000 + i))
        [await communicator.receive_json_from() for communicator in communicators_1]

    for communicator in communicators_1:
        data = await communicator.receive_json_from()
        assert "tournament_id" in data

    # トーナメント開始後、トーナメントマッチングルームにユーザーが存在しないか
    assert len(Tmm.get_waiting_users()) == 0

    communicators_2 = []
    for i in range(Tmc.ROOM_CAPACITY):
        communicators_2.append(await create_communicator(20000 + i))
        [await communicator.receive_json_from() for communicator in communicators_2]

    for communicator in communicators_2:
        data = await communicator.receive_json_from()
        assert "tournament_id" in data

    # communicators_2に対するトーナメント開始情報がcommunicators_1にSendされていないか
    for communicator in communicators_1:
        assert await communicator.receive_nothing(timeout=0.1, interval=0.01) is True

    for communicator in communicators_1:
        await communicator.disconnect()

    for communicator in communicators_2:
        await communicator.disconnect()


@pytest.mark.asyncio(loop_scope="function")
@pytest.mark.django_db
@pytest.mark.usefixtures("update_matches_data_mocker")
async def test_create_resource(create_match_records_mocker):
    """トーナメント開始後、リソースが作成されたか"""
    communicators = []
    for i in range(Tmc.ROOM_CAPACITY):
        communicators.append(await create_communicator(10000 + i))
        [await communicator.receive_json_from() for communicator in communicators]

    tournament_id = await communicators[0].receive_json_from()
    tournament_id = int(tournament_id["tournament_id"])

    for communicator in communicators:
        await communicator.disconnect()

    assert TournamentSession.search(tournament_id) is not None


@pytest.mark.asyncio(loop_scope="function")
@pytest.mark.django_db
@pytest.mark.usefixtures("update_matches_data_mocker")
async def test_start_after_timer_cancel(create_match_records_mocker):
    """
    2人の状態で1人抜け、トーナメント強制開始タイマーがcancelされた後、トーナメントが正常に開始されるか
    """
    communicators = []
    # 2人が待機している状態
    for i in range(2):
        communicators.append(await create_communicator(10000 + i))
        [await communicator.receive_json_from() for communicator in communicators]

    # １人ルームから出る
    await communicators[1].disconnect()
    del communicators[1]

    # 残っているユーザーに{"tournament_start_time": "None"}がSend
    await communicators[0].receive_json_from()

    # トーナメント開始できるまでWebSocketを作成
    for i in range(1, Tmc.ROOM_CAPACITY):
        communicators.append(await create_communicator(10000 + i))
        [await communicator.receive_json_from() for communicator in communicators]

    # tournament_idが正常に送信されたか
    for communicator in communicators:
        data = await communicator.receive_json_from()
        assert "tournament_id" in data

    for communicator in communicators:
        await communicator.disconnect()


@pytest.mark.asyncio(loop_scope="function")
@pytest.mark.django_db
@pytest.mark.usefixtures("update_matches_data_mocker")
async def test_receive_matching_wait_user_ids():
    """
    マッチング待機中ユーザーのIDが送信されるか
    TODO ポート番号 -> userIdを用いたユーザーの識別に変更時、このテストも変更する
    """
    communicator1 = await create_communicator(10000)

    data1 = await communicator1.receive_json_from()
    assert data1["wait_user_ids"] == "[10000]"

    communicator2 = await create_communicator(20000)

    data2 = await communicator1.receive_json_from()
    assert data2["wait_user_ids"] == "[10000, 20000]"

    data3 = await communicator2.receive_json_from()
    assert data3["wait_user_ids"] == "[10000, 20000]"

    await communicator1.disconnect()

    data4 = await communicator2.receive_json_from()
    assert data4["wait_user_ids"] == "[20000]"

    await communicator2.disconnect()


@pytest.mark.asyncio(loop_scope="function")
@pytest.mark.django_db
@pytest.mark.usefixtures("update_matches_data_mocker")
async def test_create_match_error(create_match_records_error_mocker):
    """Matchリソース作成処理が失敗する場合、NoneがSendされる"""
    communicators = []
    for i in range(Tmc.ROOM_CAPACITY):
        communicators.append(await create_communicator(10000 + i))
        # tournament_start_timeの通知はWebSocketが作成されるたびにルーム内の全員にSendされる
        [await communicator.receive_json_from() for communicator in communicators]

    for communicator in communicators:
        data = await communicator.receive_json_from()
        assert data["tournament_id"] == "None"

    for communicator in communicators:
        await communicator.disconnect()
