import unittest

from core.pingpong import PingPong, Player, Paddle, Ball, Screen


class TestBall(unittest.TestCase):
    def setUp(self):
        self.ball = Ball()
        self.left_player = Player(
            1, Paddle(Screen.HIGHEST_POS.value, Screen.HEIGHT.value / 2)
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
        self.ball.x_pos = Screen.LEFTEST_POS.value
        self.ball.y_pos = self.left_player.paddle.y_pos + (
            self.left_player.paddle.HEIGHT / 2
        )
        old_speed = self.ball.x_speed
        self.ball.hit_paddle(self.left_player.paddle, self.right_player.paddle)
        self.assertEqual(self.ball.x_speed, -old_speed * self.ball.ACCELERATION)

    def test_hit_left_paddle_edge_top(self):
        """ボールが左パドルの上端に当たるケース"""
        self.ball.x_pos = Screen.LEFTEST_POS.value
        # パドルの上端ぎりぎり
        self.ball.y_pos = self.left_player.paddle.y_pos - self.ball.HEIGHT + 1
        old_speed = self.ball.x_speed

        self.ball.hit_paddle(self.left_player.paddle, self.right_player.paddle)
        self.assertEqual(self.ball.x_speed, -old_speed * self.ball.ACCELERATION)

    def test_hit_left_paddle_edge_bottom(self):
        """ボールが左パドルの下端に当たるケース"""
        self.ball.x_pos = Screen.LEFTEST_POS.value  # ボールを左端に配置
        # パドルの下端ぎりぎり
        self.ball.y_pos = (
            self.left_player.paddle.y_pos + self.left_player.paddle.HEIGHT - 1
        )
        old_speed = self.ball.x_speed

        self.ball.hit_paddle(self.left_player.paddle, self.right_player.paddle)
        self.assertEqual(self.ball.x_speed, -old_speed * self.ball.ACCELERATION)
