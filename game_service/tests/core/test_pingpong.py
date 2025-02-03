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
