import unittest

from core.pingpong import PingPong, Player, Paddle, Ball, Screen


class TestBall(unittest.TestCase):
    def setUp(self):
        self.ball = Ball()
        self.left_player = Player(
            1, Paddle(Screen.LEFTEST_POS.value, Screen.HEIGHT.value / 2)
        )
        self.right_player = Player(
            2, Paddle(Screen.WIDTH.value, Screen.HEIGHT.value / 2)
        )

    def test_hit_wall_top(self):
        self.ball.y_pos = Screen.HIGHEST_POS.value
        old_speed = self.ball.y_speed
        self.ball.hit_wall()
        self.assertEqual(self.ball.y_speed, -old_speed)

    def test_hit_wall_bottom(self):
        self.ball.y_pos = Screen.HEIGHT.value - Ball.HEIGHT
        old_speed = self.ball.y_speed
        self.ball.hit_wall()
        self.assertEqual(self.ball.y_speed, -old_speed)

    def test_hit_wall_does_not_hit1(self):
        self.ball.y_pos = Screen.HEIGHT.value - Ball.HEIGHT - 1
        old_speed = self.ball.y_speed
        self.ball.hit_wall()
        self.assertEqual(self.ball.y_speed, old_speed)

    def test_hit_wall_does_not_hit2(self):
        self.ball.y_pos = Screen.HIGHEST_POS.value + 1
        old_speed = self.ball.y_speed
        self.ball.hit_wall()
        self.assertEqual(self.ball.y_speed, old_speed)

    def test_hit_wall_does_not_hit3(self):
        self.ball.y_pos = Screen.HEIGHT.value / 2
        old_speed = self.ball.y_speed
        self.ball.hit_wall()
        self.assertEqual(self.ball.y_speed, old_speed)

    def test_hit_left_paddle(self):
        self.ball.x_pos = Screen.LEFTEST_POS.value + Paddle.WIDTH
        self.ball.y_pos = self.left_player.paddle.y_pos + (
            self.left_player.paddle.HEIGHT / 2
        )
        old_speed = self.ball.x_speed
        self.ball.hit_paddle(self.left_player.paddle, self.right_player.paddle)
        self.assertEqual(self.ball.x_speed, -old_speed * self.ball.ACCELERATION)

    def test_hit_left_paddle_edge_top(self):
        """ボールが左パドルの上端に当たるケース"""
        self.ball.x_pos = Screen.LEFTEST_POS.value + Paddle.WIDTH
        # パドルの上端ぎりぎり
        self.ball.y_pos = self.left_player.paddle.y_pos - self.ball.HEIGHT + 1
        old_speed = self.ball.x_speed

        self.ball.hit_paddle(self.left_player.paddle, self.right_player.paddle)
        self.assertEqual(self.ball.x_speed, -old_speed * self.ball.ACCELERATION)

    def test_hit_left_paddle_edge_bottom(self):
        """ボールが左パドルの下端に当たるケース"""
        self.ball.x_pos = Screen.LEFTEST_POS.value + Paddle.WIDTH
        # パドルの下端ぎりぎり
        self.ball.y_pos = (
            self.left_player.paddle.y_pos + self.left_player.paddle.HEIGHT - 1
        )
        old_speed = self.ball.x_speed

        self.ball.hit_paddle(self.left_player.paddle, self.right_player.paddle)
        self.assertEqual(self.ball.x_speed, -old_speed * self.ball.ACCELERATION)

    def test_hit_left_paddle_no_hit1(self):
        """ボールが左パドルに当たらないケース"""
        self.ball.x_pos = Screen.LEFTEST_POS.value + Paddle.WIDTH
        self.ball.y_pos = self.left_player.paddle.y_pos - self.ball.HEIGHT
        old_speed = self.ball.x_speed

        self.ball.hit_paddle(self.left_player.paddle, self.right_player.paddle)
        self.assertEqual(self.ball.x_speed, old_speed)

    def test_hit_left_paddle_edge_no_hit2(self):
        """ボールが左パドルに当たらないケース"""
        self.ball.x_pos = Screen.LEFTEST_POS.value + Paddle.WIDTH
        self.ball.y_pos = self.left_player.paddle.y_pos + self.left_player.paddle.HEIGHT
        old_speed = self.ball.x_speed

        self.ball.hit_paddle(self.left_player.paddle, self.right_player.paddle)
        self.assertEqual(self.ball.x_speed, old_speed)

    def test_hit_right_paddle(self):
        self.ball.x_pos = Screen.LEFTEST_POS.value + Paddle.WIDTH
        self.ball.y_pos = self.right_player.paddle.y_pos + (
            self.right_player.paddle.HEIGHT / 2
        )
        old_speed = self.ball.x_speed
        self.ball.hit_paddle(self.left_player.paddle, self.right_player.paddle)
        self.assertEqual(self.ball.x_speed, -old_speed * self.ball.ACCELERATION)

    def test_hit_right_paddle_edge_top(self):
        """ボールが右パドルの上端に当たるケース"""
        self.ball.x_pos = Screen.LEFTEST_POS.value + Paddle.WIDTH
        self.ball.y_pos = self.right_player.paddle.y_pos + Ball.HEIGHT + 1
        old_speed = self.ball.x_speed
        self.ball.hit_paddle(self.left_player.paddle, self.right_player.paddle)
        self.assertEqual(self.ball.x_speed, -old_speed * self.ball.ACCELERATION)

    def test_hit_right_paddle_edge_bottom(self):
        """ボールが右パドルの下端に当たるケース"""
        self.ball.x_pos = Screen.LEFTEST_POS.value + Paddle.WIDTH
        self.ball.y_pos = self.right_player.paddle.y_pos + Paddle.HEIGHT - 1
        old_speed = self.ball.x_speed
        self.ball.hit_paddle(self.left_player.paddle, self.right_player.paddle)
        self.assertEqual(self.ball.x_speed, -old_speed * self.ball.ACCELERATION)

    def test_hit_right_paddle_no_hit1(self):
        """ボールが右パドルに当たらないケース"""
        self.ball.x_pos = Screen.LEFTEST_POS.value + Paddle.WIDTH
        self.ball.y_pos = self.right_player.paddle.y_pos + Paddle.HEIGHT
        old_speed = self.ball.x_speed
        self.ball.hit_paddle(self.left_player.paddle, self.right_player.paddle)
        self.assertEqual(self.ball.x_speed, old_speed)

    def test_hit_right_paddle_no_hit2(self):
        """ボールが右パドルに当たらないケース"""
        self.ball.x_pos = Screen.LEFTEST_POS.value + Paddle.WIDTH
        self.ball.y_pos = self.right_player.paddle.y_pos - Ball.HEIGHT
        old_speed = self.ball.x_speed
        self.ball.hit_paddle(self.left_player.paddle, self.right_player.paddle)
        self.assertEqual(self.ball.x_speed, old_speed)

    def test_move_no_goal(self):
        """ボールが中央付近を移動する場合、ゴールしない"""
        self.ball.x_pos = Screen.WIDTH.value // 2
        self.ball.y_pos = Screen.HEIGHT.value // 2
        old_x_pos = self.ball.x_pos
        old_y_pos = self.ball.y_pos

        goal, scorer = self.ball.move(self.left_player, self.right_player)
        self.assertEqual(self.ball.x_pos, old_x_pos + self.ball.x_speed)
        self.assertEqual(self.ball.y_pos, old_y_pos + self.ball.y_speed)
        self.assertFalse(goal)
        self.assertIsNone(scorer)

    def test_move_goal_right(self):
        """ボールが右端に到達し、左プレイヤーの得点になる"""
        self.ball.x_pos = Screen.WIDTH.value - self.ball.WIDTH - 1
        self.ball.x_speed = 4
        goal, scorer = self.ball.move(self.left_player, self.right_player)
        # goalしても描画のため、falseになる
        # 次のmoveでgoalになる
        self.assertFalse(goal)
        self.assertIsNone(scorer)

        goal, scorer = self.ball.move(self.left_player, self.right_player)
        self.assertTrue(goal)
        self.assertEqual(scorer, self.left_player)

    def test_move_goal_left(self):
        """ボールが左端に到達し、左プレイヤーの得点になる"""
        self.ball.x_pos = Screen.LEFTEST_POS.value + 4
        self.ball.x_speed = -4
        goal, scorer = self.ball.move(self.left_player, self.right_player)
        # goalしても描画のため、falseになる
        # 次のmoveでgoalになる
        self.assertFalse(goal)
        self.assertIsNone(scorer)

        goal, scorer = self.ball.move(self.left_player, self.right_player)
        self.assertTrue(goal)
        self.assertEqual(scorer, self.right_player)


class TestPaddle(unittest.TestCase):
    def setUp(self):
        self.paddle = Paddle(Screen.LEFTEST_POS.value, Screen.HEIGHT.value / 2)

    def test_move_up(self):
        old_pos = self.paddle.y_pos
        self.paddle.move_up()
        self.assertEqual(self.paddle.y_pos, old_pos - self.paddle.SPEED)

    def test_move_up_limit(self):
        self.paddle.y_pos = Screen.HIGHEST_POS.value + 5
        self.paddle.move_up()
        self.assertEqual(self.paddle.y_pos, Screen.HIGHEST_POS.value)

    def test_move_up_already_top(self):
        self.paddle.y_pos = Screen.HIGHEST_POS.value
        self.paddle.move_up()
        self.assertEqual(self.paddle.y_pos, Screen.HIGHEST_POS.value)

    def test_move_down(self):
        old_pos = self.paddle.y_pos
        self.paddle.move_down()
        self.assertEqual(self.paddle.y_pos, old_pos + self.paddle.SPEED)

    def test_move_down_limit(self):
        self.paddle.y_pos = Paddle.LOWEST_POSITION - 5
        self.paddle.move_down()
        self.assertEqual(self.paddle.y_pos, Paddle.LOWEST_POSITION)

    def test_move_down_already_bottom(self):
        self.paddle.y_pos = Paddle.LOWEST_POSITION
        self.paddle.move_down()
        self.assertEqual(self.paddle.y_pos, Paddle.LOWEST_POSITION)


class TestPingPong(unittest.TestCase):
    def setUp(self):
        self.game = PingPong()

    def setup_game(self, ball: dict, left_player: dict, right_player: dict):
        self.game.ball.x_pos = ball.get("x")
        self.game.ball.y_pos = ball.get("y")

        self.game.add_player(left_player.get("id"))
        self.game.add_player(right_player.get("id"))

        self.game.left_player.paddle.y_pos = left_player.get("y")
        self.game.left_player.score = left_player.get("score")

        self.game.right_player.paddle.y_pos = right_player.get("y")
        self.game.right_player.score = right_player.get("score")

    def test_add_player(self):
        self.assertEqual(self.game.state, PingPong.GameState.WAITING_FOR_FIRST_PLAYER)

        self.game.add_player(1)
        self.assertIsNotNone(self.game.left_player)
        self.assertIsNone(self.game.right_player)

        self.assertEqual(self.game.state, PingPong.GameState.WAITING_FOR_SECOND_PLAYER)
        self.game.add_player(2)
        self.assertEqual(self.game.state, PingPong.GameState.READY_TO_START)
        self.assertIsNotNone(self.game.left_player)
        self.assertIsNotNone(self.game.right_player)

        # 再接続時
        self.game.add_player(1)
        self.assertEqual(self.game.state, PingPong.GameState.READY_TO_START)
        self.game.add_player(2)
        self.assertEqual(self.game.state, PingPong.GameState.READY_TO_START)

    def test_add_player_reconncect(self):
        self.assertEqual(self.game.state, PingPong.GameState.WAITING_FOR_FIRST_PLAYER)
        self.game.add_player(1)
        self.assertEqual(self.game.state, PingPong.GameState.WAITING_FOR_SECOND_PLAYER)
        self.assertIsNotNone(self.game.left_player)
        self.assertIsNone(self.game.right_player)

        # 再接続時
        self.game.add_player(1)
        self.assertEqual(self.game.state, PingPong.GameState.WAITING_FOR_SECOND_PLAYER)
        self.assertIsNotNone(self.game.left_player)
        self.assertIsNone(self.game.right_player)

    def test_add_player_reconncect_in_progress(self):
        self.game.add_player(1)
        self.game.add_player(2)
        self.assertIsNotNone(self.game.left_player)
        self.assertIsNotNone(self.game.right_player)
        self.game.state = PingPong.GameState.IN_PROGRESS

        # 再接続時
        self.game.add_player(1)
        self.assertEqual(self.game.state, PingPong.GameState.IN_PROGRESS)
        self.game.add_player(2)
        self.assertEqual(self.game.state, PingPong.GameState.IN_PROGRESS)

    def test_player_action(self):
        self.game = PingPong()
        self.game.add_player(1)
        self.game.add_player(2)

        keys = self.game.left_player.keys
        upkey = keys.get(Player.UP)
        downkey = keys.get(Player.DOWN)
        left_pos = self.game.left_player.paddle.y_pos
        right_pos = self.game.right_player.paddle.y_pos

        # paddleの位置が上に移動しているはず
        self.game.player_action(1, upkey)
        self.assertTrue(self.game.left_player.paddle.y_pos < left_pos)
        # paddleの位置が下に移動しているはず
        self.game.player_action(2, downkey)
        self.assertTrue(self.game.right_player.paddle.y_pos > right_pos)

    def test_get_state(self):
        self.setup_game(
            {"x": 24, "y": 42},
            {"id": 1, "y": 7, "score": 2},
            {"id": 77, "y": 100, "score": 10},
        )

        self.assertEqual(
            self.game.get_state(),
            {
                "ball": {"x": 24, "y": 42},
                "left_player": {"id": 1, "y": 7, "score": 2},
                "right_player": {"id": 77, "y": 100, "score": 10},
            },
        )
