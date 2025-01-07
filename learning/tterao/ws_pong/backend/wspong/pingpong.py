GAME_HEIGHT = 500
GAME_WIDTH = 80


class Ball:
    HEIGHT = 20
    WIDTH = 20
    SPEED = 4
    ACCELERATION = 1.2
    LEFTEST_POS = WIDTH

    def __init__(self):
        self.x_pos = GAME_WIDTH / 2
        self.y_pos = GAME_HEIGHT / 2
        self.x_speed = self.SPEED
        self.y_speed = self.SPEED

    def hit_paddle(self, left_paddle, right_paddle):
        if (
            self.x_pos <= left_paddle.WIDTH
            and self.y_pos + self.WIDTH >= left_paddle.y_pos
            and self.y_pos <= left_paddle.y_pos + left_paddle.HEIGHT
        ) or (
            self.x_pos >= GAME_WIDTH - right_paddle.WIDTH
            and self.y_pos + self.WIDTH >= right_paddle.y_pos
            and self.y_pos <= right_paddle.y_pos + right_paddle.HEIGHT
        ):
            self.x_speed *= -1 * self.ACCELERATION

    def hit_wall(self):
        if self.y_pos <= 0 or self.y_pos >= GAME_HEIGHT - self.HEIGHT:
            self.y_speed *= -1


class Paddle:
    SPEED = 10
    HEIGHT = 20
    LOWEST_POSITION = GAME_HEIGHT - HEIGHT

    def __init__(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos

    def move_up(self):
        if self.y_pos > 0:
            # 0以下になってほしくない
            self.y_pos = max(0, self.y_pos - self.SPEED)

    def move_down(self):
        if self.y_pos < self.LOWEST_POSITION:
            self.y_pos = min(self.LOWEST_POSITION, self.y_pos - self.SPEED)


class PingPong:
    def __init__(self):
        self.ball = Ball()
