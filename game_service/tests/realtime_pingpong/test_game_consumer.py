import asyncio
from datetime import timedelta

from channels.testing import WebsocketCommunicator
import pytest
import jwt

from core.pingpong import PingPong, Player, Screen
from game_app.asgi import application
from core.match_manager import MatchManager
from realtime_pingpong import game_controller
from realtime_pingpong.consumers import ActionHandler, GameConsumer
from realtime_pingpong.game_controller import GameController


# class TestGameConsumer(unittest.IsolatedAsyncioTestCase):
#     @patch("channels.layers.get_channel_layer", return_value=MagicMock())
#     async def test_finish_game(self, mock_get_channel_layer):
#         MatchManager.remove_match = MagicMock(return_value=None)
#
#         await GameConsumer.finish_game(
#             {
#                 "matchId": 1,
#                 "results": [
#                     {"userId": 1, "score": 2},
#                     {"userId": 2, "score": 6},
#                 ],
#             },
#             "1",
#         )
#         MatchManager.remove_match.assert_called_once_with(1)
#


@pytest.mark.asyncio
class TestGameConsumer:
    async def setup(self, default_player=True):
        MatchManager.delete_all_matches()
        self.match_id = 1
        self.player_ids = [1, 2]
        self.create_match(self.match_id, self.player_ids)
        self.clients = list()
        if default_player:
            self.client1, self.client1_connected = await self.create_communicator(
                self.match_id, self.player_ids[0]
            )
            self.client2, self.client2_connected = await self.create_communicator(
                self.match_id, self.player_ids[1]
            )
        GameController.GAME_TIME_SEC = 1

    async def teardown(self):
        for client in self.clients:
            await client.disconnect()
        match = MatchManager.get_match(self.match_id)
        if match is not None:
            game_controller = match[MatchManager.KEY_GAME_CONTROLLER]
            game_controller.stop_game()
        # メンバ変数すべてを削除
        self.__dict__.clear()

    async def disconnect_client(self, client):
        await client.disconnect()
        self.clients.remove(client)

    def create_jwt_for_user(self, user_id):
        payload = {
            "user_id": user_id,
            "exp": timedelta(days=1).total_seconds(),
            "iat": timedelta(days=0).total_seconds(),
        }
        secret_key = "your_secret_key"
        token = jwt.encode(payload, secret_key, algorithm="HS256")
        return token

    def create_match(self, match_id, users):
        MatchManager.create_match(match_id, users)

    def get_uri(self, match_id):
        return f"/games/ws/enter-room/{match_id}"

    async def create_communicator(self, match_id, user_id):
        communicator = WebsocketCommunicator(application, self.get_uri(match_id))
        access_token = self.create_jwt_for_user(user_id)
        communicator.scope["cookies"] = {"access_token": access_token}
        connected, _ = await communicator.connect()
        if connected:
            self.clients.append(communicator)
        return communicator, connected

    def assert_open_message(self, actual):
        assert actual.get("message") == GameConsumer.MessageType.MSG_TIMER
        assert actual.get("end_time") is not None
        assert actual.get("type") == "game.message"

    def assert_game_message(self, actual, expect_left_id, expect_right_id):
        assert actual.get("message") == GameConsumer.MessageType.MSG_UPDATE
        assert actual.get("type") == "game.message"

        data = actual.get("data")
        assert data is not None
        state = data.get("state")
        assert state is not None

        ball = state.get("ball")
        assert ball is not None
        assert ball.get("x") is not None
        assert ball.get("y") is not None

        left_player = state.get("left_player")
        assert left_player is not None
        assert left_player.get("id") == expect_left_id
        assert left_player.get("y") is not None
        assert left_player.get("score") is not None

        right_player = state.get("right_player")
        assert right_player is not None
        assert right_player.get("id") == expect_right_id
        assert right_player.get("y") is not None
        assert right_player.get("score") is not None

    def assert_gameover_message(self, actual, player_ids):
        assert actual.get("message") == GameConsumer.MessageType.MSG_GAME_OVER
        assert actual.get("type") == "game.finish.message"
        assert actual.get("matchId") == self.match_id

        results = actual.get("results")
        assert results is not None
        for i, res in enumerate(results):
            assert res.get("userId") == player_ids[i]
            assert res.get("score") is not None

    async def receive_until(self, client, target_message):
        """
        欲しいメッセージタイプが来るまでloopする
        """
        while True:
            res = await client.receive_json_from()
            # updateの場合は一回receiveしたら次のメッセージのはず
            if target_message == GameConsumer.MessageType.MSG_UPDATE:
                return None
            if res.get("message") == target_message:
                return res

    async def receive_update_message_until(self, client, old_values):
        """
        playerのactionが反映されるまでreceiveを続ける
        """
        while True:
            res = await client.receive_json_from()
            actual = dict()
            for key, _ in old_values.items():
                state = res.get("data").get("state")
                actual[key] = state.get(key)
            if all(actual[key] != old_values[key] for key in actual):
                return res

    async def test_establish_ws_connection(self):
        await self.setup()
        assert self.client1_connected is True
        assert self.client2_connected is True
        await self.teardown()

    async def test_ws_open_message(self):
        await self.setup()
        for client in self.clients:
            res = await client.receive_json_from()
            self.assert_open_message(res)
        await self.teardown()

    async def test_game_message(self):
        """
        game進行中のメッセージはgameが続いている限り送られるので、1秒間テストする
        """
        await self.setup()
        for client in self.clients:
            await self.receive_until(client, GameConsumer.MessageType.MSG_UPDATE)

        start_time = asyncio.get_running_loop().time()
        # 1秒間game messageをテストする
        while (asyncio.get_running_loop().time() - start_time) < 1:
            for client in self.clients:
                res = await client.receive_json_from()
                self.assert_game_message(res, self.player_ids[0], self.player_ids[1])
        await self.teardown()

    async def test_gameover_message(self):
        """
        gameのresultメッセージとcleanup処理のテスト
        """
        await self.setup()
        responses = []
        for client in self.clients:
            responses.append(
                await self.receive_until(client, GameConsumer.MessageType.MSG_GAME_OVER)
            )
        for res in responses:
            self.assert_gameover_message(res, self.player_ids)
        assert MatchManager.get_match(self.match_id) is None
        await self.teardown()

    async def test_send_message(self):
        """
        接続さえできればメッセージは送れるはず
        sendしたメッセージがちゃんと反映されているか
        """
        await self.setup(default_player=False)
        await self.create_communicator(self.match_id, self.player_ids[0])
        # gameははじまっていないけどメッセージはおくれる.なにも起こらない
        await self.clients[0].send_json_to(
            {
                "type": ActionHandler.ACTION_PADDLE,
                "key": Player.KEY + "W",
            }
        )
        await self.create_communicator(self.match_id, self.player_ids[1])
        for client in self.clients:
            await self.receive_until(client, GameConsumer.MessageType.MSG_UPDATE)

        responses = []
        for client in self.clients:
            responses.append(await client.receive_json_from())
        # paddleの初期位置を取得
        initial_pos = dict()
        for res in responses:
            state = res.get("data").get("state")
            assert state.get("left_player").get("y") == Screen.HEIGHT / 2
            assert state.get("right_player").get("y") == Screen.HEIGHT / 2
            initial_pos["left_player"] = state.get("left_player").get("y")
            initial_pos["right_player"] = state.get("right_player").get("y")

        # それぞれパドルを逆方向に動かす
        await self.clients[0].send_json_to(
            {
                "type": ActionHandler.ACTION_PADDLE,
                "key": Player.KEY + "W",
            }
        )
        await self.clients[1].send_json_to(
            {
                "type": ActionHandler.ACTION_PADDLE,
                "key": Player.KEY + "S",
            }
        )

        responses.clear()
        for client in self.clients:
            responses.append(
                await self.receive_update_message_until(client, initial_pos)
            )
        # paddleの位置がちゃんと移動しているか
        for res in responses:
            state = res.get("data").get("state")
            assert state.get("left_player").get("y") < initial_pos.get("left_player")
            assert state.get("right_player").get("y") > initial_pos.get("right_player")
        await self.teardown()

    async def test_send_random_message(self):
        """
        適当なメッセージを送ってもcrashしない
        """
        await self.setup()
        await self.clients[0].send_json_to(
            {
                "random": "hello world",
            }
        )
        await self.clients[1].send_json_to(
            {
                "type": ActionHandler.ACTION_PADDLE,
                "key": "randomkey",
            }
        )
        await self.teardown()

    async def test_reconnect(self):
        """
        接続してから切断する。そのあと再接続
        """
        await self.setup()
        await self.disconnect_client(self.clients[0])
        # 再接続
        # openメッセージの後に、updateメッセージが届くはず
        client, _ = await self.create_communicator(self.match_id, self.player_ids[0])
        res = await client.receive_json_from()
        self.assert_open_message(res)
        res = await client.receive_json_from()
        self.assert_game_message(res, self.player_ids[0], self.player_ids[1])

        await self.teardown()

    async def test_error_missing_jwt(self):
        await self.setup(default_player=False)
        communicator = WebsocketCommunicator(application, self.get_uri(self.match_id))
        connected, _ = await communicator.connect()
        assert connected is False
        await self.teardown()

    async def test_error_wrong_userid(self):
        await self.setup(default_player=False)
        _, connected = await self.create_communicator(self.match_id, 3)
        assert connected is False
        await self.teardown()
