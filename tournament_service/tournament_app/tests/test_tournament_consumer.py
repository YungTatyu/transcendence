import asyncio
import pytest
from channels.testing import WebsocketCommunicator

from tournament_app.consumers.tournament_matching_consumer import (
    TournamentMatchingConsumer as Tmc,
)
from tournament_app.consumers.tournament_consumer import TournamentConsumer
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
    communicator = WebsocketCommunicator(TournamentConsumer.as_asgi(), path)
    communicator.scope["url_route"] = {"kwargs": {"tournamentId": tournament_id}}
    connected, _ = await communicator.connect()
    assert connected
    return communicator


@pytest.mark.asyncio(loop_scope="function")
@pytest.mark.django_db
async def test_tournament_4_participants(
    create_match_records_mocker,
    dummy_matches_data_mocker,
    mock_handle_tournament_match_bye,
):
    # トーナメントマッチングルームに入り、tournament_idを取得
    comms = []
    for i in range(Tmc.ROOM_CAPACITY):
        comms.append(await create_communicator(10000 + i))
        [await communicator.receive_json_from() for communicator in comms]

    tournament_id = await comms[0].receive_json_from()
    tournament_id = int(tournament_id["tournament_id"])

    for communicator in comms:
        await communicator.disconnect()

    # トーナメントルームに入り、試合が展開される
    tournament_comms = []
    for _ in range(Tmc.ROOM_CAPACITY):
        communicator = await create_tournament_communicator(tournament_id)
        res = await communicator.receive_json_from()
        tournament_comms.append(communicator)
        print("\n\n[1]", res)

    await asyncio.sleep(TournamentSession.LIMIT_TOURNAMENT_MATCH_SEC + 1)
    for communicator in tournament_comms:
        res = await communicator.receive_json_from()
        print("\n\n[2]", res)

    for communicator in tournament_comms:
        await communicator.disconnect()
    TournamentSession.clear()
