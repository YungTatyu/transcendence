import asyncio

import pytest
from channels.testing import WebsocketCommunicator

from tournament_app.consumers.tournament_consumer import TournamentConsumer
from tournament_app.consumers.tournament_matching_consumer import (
    TournamentMatchingConsumer as Tmc,
)
from tournament_app.consumers.tournament_state import TournamentState
from tournament_app.utils.tournament_session import TournamentSession

PATH_MATCHING = "/tournament/ws/enter-room"
FORMAT_TOURNAMENT = "/tournament/ws/enter-room/{}"


class CustomWebsocketCommunicator(WebsocketCommunicator):
    def __init__(self, application, path, scope_override=None):
        super().__init__(application, path)
        if scope_override:
            self.scope.update(scope_override)


async def create_communicator(port: int):
    communicator = CustomWebsocketCommunicator(
        Tmc.as_asgi(),
        PATH_MATCHING,
        scope_override={"client": ("127.0.0.1", port)},
    )
    connected, _ = await communicator.connect()
    assert connected
    return communicator


async def create_tournament_communicator(tournament_id: int):
    path = FORMAT_TOURNAMENT.format(tournament_id)
    communicator = CustomWebsocketCommunicator(
        TournamentConsumer.as_asgi(),
        path,
        scope_override={"url_route": {"kwargs": {"tournamentId": tournament_id}}},
    )
    connected, _ = await communicator.connect()
    assert connected
    return communicator


@pytest.fixture()
async def setup_finished_matching(mock_limit_tournament_match_sec) -> int:
    """トーナメントマッチングルームに入り、マッチング終了後tournament_idを取得"""
    comms = []
    for i in range(Tmc.ROOM_CAPACITY):
        comms.append(await create_communicator(10000 + i))
        [await communicator.receive_json_from() for communicator in comms]

    tournament_id = await comms[0].receive_json_from()
    tournament_id = int(tournament_id["tournament_id"])

    for communicator in comms:
        await communicator.disconnect()

    return tournament_id


@pytest.mark.django_db
async def request_tournament_match_finish_imitate(tournament_id, round):
    """トーナメント試合終了APIを叩く処理を模倣する"""
    tournament_session = TournamentSession.search(tournament_id)
    if tournament_session is None:
        raise Exception
    if tournament_session.current_round != round:
        raise Exception
    await tournament_session.update_tournament_session_info()


@pytest.mark.asyncio(loop_scope="function")
@pytest.mark.django_db
async def test_tournament_auto_execution(
    create_match_records_mocker,
    dummy_matches_data_mocker,
    mock_handle_tournament_match_bye,
    mock_limit_tournament_match_sec,
    setup_finished_matching,
):
    """強制勝ち上がり処理によって自動的にトーナメントが進行"""
    tournament_id = setup_finished_matching
    tournament_comms = []
    for _ in range(Tmc.ROOM_CAPACITY):
        communicator = await create_tournament_communicator(tournament_id)
        tournament_comms.append(communicator)
        res = await communicator.receive_json_from()
        assert res["current_round"] == 1
        assert res["state"] == TournamentState.ONGOING

    # round1の強制勝ち上がり処理が自動実行される
    await asyncio.sleep(TournamentSession.LIMIT_TOURNAMENT_MATCH_SEC + 0.1)
    for communicator in tournament_comms:
        res = await communicator.receive_json_from()
        assert res["current_round"] == 2
        assert res["state"] == TournamentState.ONGOING

    # round2の強制勝ち上がり処理が自動実行される
    await asyncio.sleep(TournamentSession.LIMIT_TOURNAMENT_MATCH_SEC + 0.1)
    for communicator in tournament_comms:
        res = await communicator.receive_json_from()
        assert res["current_round"] == 3
        assert res["state"] == TournamentState.ONGOING

    # round3(決勝戦)の強制勝ち上がり処理が自動実行される
    await asyncio.sleep(TournamentSession.LIMIT_TOURNAMENT_MATCH_SEC + 0.1)
    for communicator in tournament_comms:
        res = await communicator.receive_json_from()
        assert res["state"] == TournamentState.FINISHED

    for communicator in tournament_comms:
        await communicator.disconnect()
    TournamentSession.clear()


@pytest.mark.asyncio(loop_scope="function")
@pytest.mark.django_db
async def test_tournament_manual_execution(
    create_match_records_mocker,
    dummy_matches_data_mocker,
    mock_handle_tournament_match_bye,
    setup_finished_matching,
):
    """tournaments/finish-matchエンドポイントを叩くことよってトーナメントが進行"""
    tournament_id = setup_finished_matching
    tournament_comms = []
    for _ in range(Tmc.ROOM_CAPACITY):
        communicator = await create_tournament_communicator(tournament_id)
        tournament_comms.append(communicator)
        res = await communicator.receive_json_from()
        assert res["current_round"] == 1
        assert res["state"] == TournamentState.ONGOING

    # round1の手動トーナメント試合終了処理で次の試合に進む
    await request_tournament_match_finish_imitate(tournament_id, 1)
    for communicator in tournament_comms:
        res = await communicator.receive_json_from()
        assert res["current_round"] == 2
        assert res["state"] == TournamentState.ONGOING

    # round2の手動トーナメント試合終了処理で次の試合に進む
    await request_tournament_match_finish_imitate(tournament_id, 2)
    for communicator in tournament_comms:
        res = await communicator.receive_json_from()
        assert res["current_round"] == 3
        assert res["state"] == TournamentState.ONGOING

    # round3(決勝戦)の手動トーナメント試合終了処理で次の試合に進む
    await request_tournament_match_finish_imitate(tournament_id, 3)
    for communicator in tournament_comms:
        res = await communicator.receive_json_from()
        assert res["state"] == TournamentState.FINISHED

    for communicator in tournament_comms:
        await communicator.disconnect()
    TournamentSession.clear()


@pytest.mark.asyncio(loop_scope="function")
@pytest.mark.django_db
async def test_tournament_manual_and_auto_execution(
    create_match_records_mocker,
    dummy_matches_data_mocker,
    mock_handle_tournament_match_bye,
    mock_limit_tournament_match_sec,
    setup_finished_matching,
):
    """
    round1はtournaments/finish-matchが叩かれることによる手動処理
    round2,round3はTaskTimerによる自動勝ち上がり処理
    """
    tournament_id = setup_finished_matching
    tournament_comms = []
    for _ in range(Tmc.ROOM_CAPACITY):
        communicator = await create_tournament_communicator(tournament_id)
        tournament_comms.append(communicator)
        res = await communicator.receive_json_from()
        assert res["current_round"] == 1
        assert res["state"] == TournamentState.ONGOING

    # round1の手動トーナメント試合終了処理で次の試合に進む
    await request_tournament_match_finish_imitate(tournament_id, 1)
    for communicator in tournament_comms:
        res = await communicator.receive_json_from()
        assert res["current_round"] == 2
        assert res["state"] == TournamentState.ONGOING

    # round2の強制勝ち上がり処理が自動実行される
    await asyncio.sleep(TournamentSession.LIMIT_TOURNAMENT_MATCH_SEC + 0.1)
    for communicator in tournament_comms:
        res = await communicator.receive_json_from()
        assert res["current_round"] == 3
        assert res["state"] == TournamentState.ONGOING

    # round3(決勝戦)の強制勝ち上がり処理が自動実行される
    await asyncio.sleep(TournamentSession.LIMIT_TOURNAMENT_MATCH_SEC + 0.1)
    for communicator in tournament_comms:
        res = await communicator.receive_json_from()
        assert res["state"] == TournamentState.FINISHED

    for communicator in tournament_comms:
        await communicator.disconnect()
    TournamentSession.clear()


@pytest.mark.asyncio(loop_scope="function")
@pytest.mark.django_db
async def test_tournament_manual_and_auto_execution_enter_one_user(
    create_match_records_mocker,
    dummy_matches_data_mocker,
    mock_handle_tournament_match_bye,
    mock_limit_tournament_match_sec,
    setup_finished_matching,
):
    """
    参加者4人に対して、トーナメントルームに入る人数は1人だけのケース
    """
    tournament_id = setup_finished_matching
    communicator = await create_tournament_communicator(tournament_id)
    res = await communicator.receive_json_from()
    assert res["current_round"] == 1
    assert res["state"] == TournamentState.ONGOING

    # round1の手動トーナメント試合終了処理で次の試合に進む
    await request_tournament_match_finish_imitate(tournament_id, 1)
    res = await communicator.receive_json_from()
    assert res["current_round"] == 2
    assert res["state"] == TournamentState.ONGOING

    # round2の強制勝ち上がり処理が自動実行される
    await asyncio.sleep(TournamentSession.LIMIT_TOURNAMENT_MATCH_SEC + 0.1)
    res = await communicator.receive_json_from()
    assert res["current_round"] == 3
    assert res["state"] == TournamentState.ONGOING

    # round3(決勝戦)の強制勝ち上がり処理が自動実行される
    await asyncio.sleep(TournamentSession.LIMIT_TOURNAMENT_MATCH_SEC + 0.1)
    res = await communicator.receive_json_from()
    assert res["state"] == TournamentState.FINISHED

    await communicator.disconnect()
    TournamentSession.clear()


@pytest.mark.asyncio(loop_scope="function")
@pytest.mark.django_db
async def test_fetch_matches_data_error(
    create_match_records_mocker,
    mock_fetch_matches_data,
    mock_handle_tournament_match_bye,
    mock_limit_tournament_match_sec,
    setup_finished_matching,
):
    """
    matchesエンドポイントからデータの取得が失敗した場合
    response["state"]がerrorとなる
    """
    tournament_id = setup_finished_matching

    tournament_comms = []
    for _ in range(Tmc.ROOM_CAPACITY):
        communicator = await create_tournament_communicator(tournament_id)
        tournament_comms.append(communicator)
        res = await communicator.receive_json_from()
        assert res["current_round"] == 1
        assert res["state"] == TournamentState.ONGOING

    # round1の手動トーナメント試合終了処理で次の試合に進む
    await request_tournament_match_finish_imitate(tournament_id, 1)
    for communicator in tournament_comms:
        res = await communicator.receive_json_from()
        assert res["current_round"] == 2
        # update_matches_dataが失敗し、errorが返る
        assert res["state"] == TournamentState.ERROR

    for communicator in tournament_comms:
        await communicator.disconnect()
    TournamentSession.clear()


@pytest.mark.asyncio(loop_scope="function")
@pytest.mark.django_db
async def test_fetch_tournament_match_finish_error(
    create_match_records_mocker,
    dummy_matches_data_mocker,
    mock_fetch_tournament_match_finish,
    mock_limit_tournament_match_sec,
    setup_finished_matching,
):
    """
    matches/finish エンドポイントを叩く処理が失敗した場合
    response["state"]がerrorとなる
    """
    tournament_id = setup_finished_matching

    tournament_comms = []
    for _ in range(Tmc.ROOM_CAPACITY):
        communicator = await create_tournament_communicator(tournament_id)
        tournament_comms.append(communicator)
        res = await communicator.receive_json_from()
        assert res["current_round"] == 1
        assert res["state"] == TournamentState.ONGOING

    # TaskTimerによる強制勝ち上がり処理が実行される
    await asyncio.sleep(TournamentSession.LIMIT_TOURNAMENT_MATCH_SEC + 0.1)

    for communicator in tournament_comms:
        res = await communicator.receive_json_from()
        # handle_tournament_match_byeが失敗し、errorが返る
        assert res["state"] == TournamentState.ERROR

    for communicator in tournament_comms:
        await communicator.disconnect()
    TournamentSession.clear()


@pytest.mark.asyncio(loop_scope="function")
@pytest.mark.django_db
async def test_no_tournament_session(
    create_match_records_mocker,
    dummy_matches_data_mocker,
    mock_handle_tournament_match_bye,
    mock_limit_tournament_match_sec,
):
    """
    TournamentSessionが作成されていないケース
    """
    tournament_id = 12345
    communicator = CustomWebsocketCommunicator(
        TournamentConsumer.as_asgi(),
        FORMAT_TOURNAMENT.format(tournament_id),
        scope_override={"url_route": {"kwargs": {"tournamentId": tournament_id}}},
    )
    connected, _ = await communicator.connect()
    assert not connected  # 接続が拒否されたかを確認
    TournamentSession.clear()
