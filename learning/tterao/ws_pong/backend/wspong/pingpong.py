from collections import namedtuple
from enum import Enum, auto

Position = namedtuple("Position", ["x", "y"])

GAME_HEIGHT = 500
GAME_WIDTH = 80
GAME_HIGHEST_POS = 0
GAME_LEFTEST_POS = 0


class Ball:
    HEIGHT = 20
    WIDTH = 20
    INITIAL_POS = Position(x=GAME_WIDTH / 2, y=GAME_HEIGHT / 2)
    INITIAL_SPEED = Position(x=4, y=4)
    ACCELERATION = 1.2
    LEFTEST_POS = WIDTH

    def __init__(self):
        self.x_pos, self.y_pos = self.INITIAL_POS
        self.x_speed, self.y_speed = self.INITIAL_SPEED

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
        if self.y_pos <= GAME_HIGHEST_POS or self.y_pos >= GAME_HEIGHT - self.HEIGHT:
            self.y_speed *= -1

    def move(self, left_player, right_player):
        """
        ゴールしたら、Trueとゴールしたplayerを返す
        """
        self.x_pos = self.adjust_limit(
            self.x_pos + self.x_speed, GAME_WIDTH - self.WIDTH
        )
        self.y_pos = self.adjust_limit(
            self.y_pos + self.y_speed, GAME_HEIGHT - self.HEIGHT
        )
        self.hit_paddle(left_player.paddle, right_player.paddle)
        self.hit_wall()
        if self.x_pos >= GAME_WIDTH - self.WIDTH:
            return (True, left_player)
        elif self.y_pos <= GAME_LEFTEST_POS:
            return (True, right_player)
        return (False, None)

    def adjust_limit(self, pos, limit):
        """
        ballがgameの範囲を越えないように調整する
        """
        if pos <= 0:
            return 0
        if pos > limit:
            return limit
        return pos

    def reset_ball_status(self):
        self.x_pos, self.y_pos = self.INITIAL_POS
        self.x_speed, self.y_speed = self.INITIAL_SPEED


class Paddle:
    SPEED = 10
    HEIGHT = 20
    LOWEST_POSITION = GAME_HEIGHT - HEIGHT

    def __init__(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos

    def move_up(self):
        if self.y_pos > GAME_HIGHEST_POS:
            # 0以下になってほしくない
            self.y_pos = max(GAME_HIGHEST_POS, self.y_pos - self.SPEED)

    def move_down(self):
        if self.y_pos < self.LOWEST_POSITION:
            self.y_pos = min(self.LOWEST_POSITION, self.y_pos - self.SPEED)


class Player:
    UP = "UP"
    DOWN = "DOWN"
    KEY = "Key"

    def __init__(self, name, paddle):
        self.name = name
        self.paddle = paddle
        self.keys = {self.UP: self.KEY + "W", self.DOWN: self.KEY + "S"}
        self.score = 0

    def move_paddle(self, key):
        actions = {
            self.keys[self.UP]: self.paddle.move_up,
            self.keys[self.DOWN]: self.paddle.move_down,
        }
        action = actions.get(key)
        if action is None:
            return
        action()

    def score(self):
        self.score += 1


class PingPong:
    class GameState(Enum):
        WAITING_FOR_FIRST_PLAYER = auto()
        WAITING_FOR_SECOND_PLAYER = auto()
        READY_TO_START = auto()
        IN_PROGRESS = auto()
        GAME_OVER = auto()

    def __init__(self, name1=None, name2=None):
        self.state = self.GameState.WAITING_FOR_FIRST_PLAYER
        self.ball = Ball()
        self.left_player = self.add_player(name1)
        self.right_player = self.add_player(name2)

    def add_player(self, name):
        if name is None:
            return None  # Noneでplayerを初期化
        if (
            self.state != self.GameState.WAITING_FOR_FIRST_PLAYER
            and self.state != self.GameState.WAITING_FOR_SECOND_PLAYER
        ):
            raise RuntimeError("this game is already ready to play.")
        if self.state == self.GameState.WAITING_FOR_FIRST_PLAYER:
            self.left_player = Player(name, Paddle(GAME_HIGHEST_POS, GAME_HEIGHT / 2))
            self.state = self.GameState.WAITING_FOR_SECOND_PLAYER
            return
        self.right_player = Player(name, Paddle(GAME_WIDTH, GAME_HEIGHT / 2))
        self.state = self.GameState.READY_TO_START

    def player_action(self, name, key):
        if name == self.left_player.name:
            self.left_player.move_paddle(key)
        elif name == self.right_player.name:
            self.right_player.move_paddle(key)

    def get_state(self):
        return {
            "ball": {"x": self.ball.x_pos, "y": self.ball.y_pos},
            self.left_player.name: {"y": self.left_player.paddle.y_pos},
            self.right_player.name: {"y": self.right_player.paddle.y_pos},
        }
