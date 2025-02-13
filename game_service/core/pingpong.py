from collections import namedtuple
from dataclasses import dataclass
from enum import Enum, auto
import random

Position = namedtuple("Position", ["x", "y"])


@dataclass(frozen=True)
class Screen:
    HEIGHT: int = 500
    WIDTH: int = 800
    HIGHEST_POS: int = 0
    LEFTEST_POS: int = 0


class Ball:
    HEIGHT = 20
    WIDTH = 20
    INITIAL_POS = Position(x=Screen.WIDTH / 2, y=Screen.HEIGHT / 2)
    INITIAL_SPEED = Position(x=4, y=4)
    ACCELERATION = 1.2
    LEFTEST_POS = Screen.LEFTEST_POS

    def __init__(self):
        self.__x_pos = self.INITIAL_POS.x
        self.__y_pos = self.INITIAL_POS.y
        self.__x_speed = (
            self.INITIAL_SPEED.x
            if random.choice([True, False])
            else self.INITIAL_SPEED.x * -1
        )
        random_speed = self.generate_random_speed()
        self.__y_speed = (
            random_speed if random.choice([True, False]) else random_speed * -1.0
        )

    @property
    def x_pos(self):
        return self.__x_pos

    @x_pos.setter
    def x_pos(self, value):
        self.__x_pos = value

    @property
    def y_pos(self):
        return self.__y_pos

    @y_pos.setter
    def y_pos(self, value):
        self.__y_pos = value

    @property
    def x_speed(self):
        return self.__x_speed

    @x_speed.setter
    def x_speed(self, value):
        self.__x_speed = value

    @property
    def y_speed(self):
        return self.__y_speed

    @y_speed.setter
    def y_speed(self, value):
        self.__y_speed = value

    def hit_paddle(self, left_paddle, right_paddle):
        if (
            self.__x_pos <= Screen.LEFTEST_POS + left_paddle.WIDTH
            and self.__y_pos + self.HEIGHT > left_paddle.y_pos
            and self.__y_pos < left_paddle.y_pos + left_paddle.HEIGHT
        ) or (
            self.__x_pos + self.WIDTH >= Screen.WIDTH - right_paddle.WIDTH
            and self.__x_pos <= Screen.WIDTH
            and self.__y_pos + self.HEIGHT > right_paddle.y_pos
            and self.__y_pos < right_paddle.y_pos + right_paddle.HEIGHT
        ):
            self.__x_speed *= -1 * self.ACCELERATION
            return True
        return False

    def hit_wall(self):
        if (
            self.__y_pos <= Screen.HIGHEST_POS
            or self.__y_pos >= Screen.HEIGHT - self.HEIGHT
        ):
            self.__y_speed *= -1

    def move(self, left_player, right_player):
        """
        ゴールしたら、Trueとゴールしたplayerを返す
        """
        # ゴールした瞬間も描画したいからballを動かしたすぐ後にゴール判定しない
        if self.__x_pos >= Screen.WIDTH - self.WIDTH:
            self.reset_ball_status()
            return (True, left_player)
        elif self.__x_pos <= Screen.LEFTEST_POS:
            self.reset_ball_status()
            return (True, right_player)

        # ballを動かす
        self.__x_pos = self.adjust_limit(
            self.__x_pos + self.__x_speed, Screen.WIDTH - self.WIDTH
        )
        self.__y_pos = self.adjust_limit(
            self.__y_pos + self.__y_speed, Screen.HEIGHT - self.HEIGHT
        )
        if self.hit_paddle(left_player.paddle, right_player.paddle):
            # goal判定されないように少しずらす
            self.__x_pos += 0.1 if self.__x_speed > 0 else -0.1

        self.hit_wall()
        return (False, None)

    def adjust_limit(self, pos, limit):
        """
        ballがgameの範囲を越えないように調整する
        """
        if pos <= Screen.LEFTEST_POS:
            return Screen.LEFTEST_POS
        if pos >= limit:
            return limit
        return pos

    def reset_ball_status(self):
        # goalをきめたプレイヤーの方向にボールが進む
        self.__x_speed = (
            self.INITIAL_SPEED.x
            if self.x_pos <= Screen.LEFTEST_POS
            else self.INITIAL_SPEED.x * -1
        )
        random_speed = self.generate_random_speed()
        self.__y_speed = (
            random_speed if random.choice([True, False]) else random_speed * -1.0
        )
        self.__x_pos = self.INITIAL_POS.x
        self.__y_pos = self.INITIAL_POS.y

    def generate_random_speed(self):
        return random.uniform(3.0, 6.0)


class Paddle:
    SPEED = 10
    HEIGHT = 100
    WIDTH = 10
    LOWEST_POSITION = Screen.HEIGHT - HEIGHT

    def __init__(self, x_pos, y_pos):
        self.__x_pos = x_pos
        self.__y_pos = y_pos

    @property
    def x_pos(self):
        return self.__x_pos

    @x_pos.setter
    def x_pos(self, value):
        self.__x_pos = value

    @property
    def y_pos(self):
        return self.__y_pos

    @y_pos.setter
    def y_pos(self, value):
        self.__y_pos = value

    def move_up(self):
        # 0以下になってほしくない
        self.__y_pos = max(Screen.HIGHEST_POS, self.__y_pos - self.SPEED)

    def move_down(self):
        self.__y_pos = min(self.LOWEST_POSITION, self.__y_pos + self.SPEED)


class Player:
    UP = "UP"
    DOWN = "DOWN"
    KEY = "Key"

    def __init__(self, id, paddle, key_up="W", key_down="S"):
        self.__id = id
        self.__paddle = paddle
        self.__keys = {self.UP: self.KEY + key_up, self.DOWN: self.KEY + key_down}
        self.__score = 0

    @property
    def id(self):
        return self.__id

    @property
    def paddle(self):
        return self.__paddle

    @property
    def keys(self):
        return self.__keys

    @property
    def score(self):
        return self.__score

    @score.setter
    def score(self, value):
        self.__score = value

    def move_paddle(self, key):
        actions = {
            self.__keys[self.UP]: self.__paddle.move_up,
            self.__keys[self.DOWN]: self.__paddle.move_down,
        }
        action = actions.get(key)
        if action is None:
            return
        action()

    def increment_score(self):
        self.__score += 1


class PingPong:
    """
    ピンポンゲームのロジックを担当する
    """

    class GameState(Enum):
        WAITING_FOR_FIRST_PLAYER = auto()
        WAITING_FOR_SECOND_PLAYER = auto()
        READY_TO_START = auto()
        IN_PROGRESS = auto()
        GAME_OVER = auto()

    def __init__(self):
        self.__state = self.GameState.WAITING_FOR_FIRST_PLAYER
        self.__ball = Ball()
        self.__left_player = None
        self.__right_player = None

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, value):
        self.__state = value

    @property
    def ball(self):
        return self.__ball

    @property
    def left_player(self):
        return self.__left_player

    @property
    def right_player(self):
        return self.__right_player

    def add_player(self, player_id):
        if (
            self.__state != self.GameState.WAITING_FOR_FIRST_PLAYER
            and self.__state != self.GameState.WAITING_FOR_SECOND_PLAYER
        ):
            # すでにプレイヤーが作成されている時はなにもしない
            return
        if self.__state == self.GameState.WAITING_FOR_FIRST_PLAYER:
            self.__left_player = Player(
                player_id, Paddle(Screen.LEFTEST_POS, Screen.HEIGHT / 2)
            )
            self.__state = self.GameState.WAITING_FOR_SECOND_PLAYER
            return
        # プレイヤーの再接続
        if self.__left_player.id == player_id:
            return
        self.__right_player = Player(player_id, Paddle(Screen.WIDTH, Screen.HEIGHT / 2))
        self.__state = self.GameState.READY_TO_START

    def player_action(self, id, key):
        if id == self.__left_player.id:
            self.__left_player.move_paddle(key)
        elif id == self.__right_player.id:
            self.__right_player.move_paddle(key)

    def get_state(self):
        return {
            "ball": {"x": self.__ball.x_pos, "y": self.__ball.y_pos},
            "left_player": {
                "id": self.__left_player.id,
                "y": self.__left_player.paddle.y_pos,
                "score": self.__left_player.score,
            },
            "right_player": {
                "id": self.__right_player.id,
                "y": self.__right_player.paddle.y_pos,
                "score": self.__right_player.score,
            },
        }

    def update(self):
        scored, player = self.__ball.move(self.__left_player, self.__right_player)
        if scored:
            player.increment_score()

    def is_match_over(self):
        return self.__left_player.score != self.__right_player.score
