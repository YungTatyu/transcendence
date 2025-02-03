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
