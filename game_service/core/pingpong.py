from collections import namedtuple
from enum import Enum, auto

Position = namedtuple("Position", ["x", "y"])


class Screen(Enum):
    HEIGHT = 500
    WIDTH = 800
    HIGHEST_POS = 0
    LEFTEST_POS = 0


class Ball:
    HEIGHT = 20
    WIDTH = 20
    INITIAL_POS = Position(x=Screen.WIDTH.value / 2, y=Screen.HEIGHT.value / 2)
    INITIAL_SPEED = Position(x=4, y=4)
    ACCELERATION = 1.2
    LEFTEST_POS = WIDTH

    def __init__(self):
        self.__x_pos = self.INITIAL_POS.x
        self.__y_pos = self.INITIAL_POS.y
        self.__x_speed = self.INITIAL_SPEED.x
        self.__y_speed = self.INITIAL_SPEED.y

    @property
    def x_pos(self):
        return self.__x_pos

    @property
    def y_pos(self):
        return self.__y_pos

    @property
    def x_speed(self):
        return self.__x_speed

    @property
    def y_speed(self):
        return self.__y_speed

    def hit_paddle(self, left_paddle, right_paddle):
        if (
            self.__x_pos <= left_paddle.WIDTH
            and self.__x_pos + self.WIDTH >= self.LEFTEST_POS
            and self.__y_pos + self.HEIGHT >= left_paddle.y_pos
            and self.__y_pos <= left_paddle.y_pos + left_paddle.HEIGHT
        ) or (
            self.__x_pos + self.WIDTH >= Screen.WIDTH.value - right_paddle.WIDTH
            and self.__x_pos <= Screen.WIDTH.value
            and self.__y_pos + self.HEIGHT >= right_paddle.y_pos
            and self.__y_pos <= right_paddle.y_pos + right_paddle.HEIGHT
        ):
            print("hit paddle")
            self.__x_speed *= -1 * self.ACCELERATION

    def hit_wall(self):
        if (
            self.__y_pos <= Screen.HIGHEST_POS.value
            or self.__y_pos >= Screen.HEIGHT.value - self.HEIGHT
        ):
            print("hit wall")
            self.__y_speed *= -1

    def move(self, left_player, right_player):
        """
        ゴールしたら、Trueとゴールしたplayerを返す
        """
        self.__x_pos = self.adjust_limit(
            self.__x_pos + self.__x_speed, Screen.WIDTH.value - self.WIDTH
        )
        self.__y_pos = self.adjust_limit(
            self.__y_pos + self.__y_speed, Screen.HEIGHT.value - self.HEIGHT
        )
        self.hit_paddle(left_player.paddle, right_player.paddle)
        self.hit_wall()
        if self.__x_pos >= Screen.WIDTH.value - self.WIDTH:
            self.reset_ball_status()
            return (True, left_player)
        elif self.__x_pos <= Screen.LEFTEST_POS.value:
            self.reset_ball_status()
            return (True, right_player)
        return (False, None)

    def adjust_limit(self, pos, limit):
        """
        ballがgameの範囲を越えないように調整する
        """
        if pos <= 0:
            return 0
        if pos >= limit:
            return limit
        return pos

    def reset_ball_status(self):
        self.__x_pos = self.INITIAL_POS.x
        self.__y_pos = self.INITIAL_POS.y
        self.__x_speed = self.INITIAL_SPEED.x
        self.__y_speed = self.INITIAL_SPEED.y


class Paddle:
    SPEED = 10
    HEIGHT = 100
    WIDTH = 10
    LOWEST_POSITION = Screen.HEIGHT.value - HEIGHT

    def __init__(self, x_pos, y_pos):
        self.__x_pos = x_pos
        self.__y_pos = y_pos

    @property
    def x_pos(self):
        return self.__x_pos

    @property
    def y_pos(self):
        return self.__y_pos

    def move_up(self):
        if self.__y_pos > Screen.HIGHEST_POS.value:
            # 0以下になってほしくない
            self.__y_pos = max(Screen.HIGHEST_POS.value, self.__y_pos - self.SPEED)

    def move_down(self):
        if self.__y_pos < self.LOWEST_POSITION:
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
    class GameState(Enum):
        WAITING_FOR_FIRST_PLAYER = auto()
        WAITING_FOR_SECOND_PLAYER = auto()
        READY_TO_START = auto()
        IN_PROGRESS = auto()
        GAME_OVER = auto()

    def __init__(self, player1=None, playerr2=None):
        self.state = self.GameState.WAITING_FOR_FIRST_PLAYER
        self.ball = Ball()
        self.left_player = self.add_player(player1)
        self.right_player = self.add_player(playerr2)

    def add_player(self, player_id):
        if player_id is None:
            return None  # Noneでplayerを初期化
        if (
            self.state != self.GameState.WAITING_FOR_FIRST_PLAYER
            and self.state != self.GameState.WAITING_FOR_SECOND_PLAYER
        ):
            raise RuntimeError("this game is already ready to play.")
        if self.state == self.GameState.WAITING_FOR_FIRST_PLAYER:
            self.left_player = Player(
                player_id, Paddle(Screen.HIGHEST_POS.value, Screen.HEIGHT.value / 2)
            )
            self.state = self.GameState.WAITING_FOR_SECOND_PLAYER
            return
        self.right_player = Player(
            player_id, Paddle(Screen.WIDTH.value, Screen.HEIGHT.value / 2)
        )
        self.state = self.GameState.READY_TO_START

    def player_action(self, id, key):
        if id == self.left_player.id:
            self.left_player.move_paddle(key)
        elif id == self.right_player.id:
            self.right_player.move_paddle(key)

    def get_state(self):
        return {
            "ball": {"x": self.ball.x_pos, "y": self.ball.y_pos},
            "left_player": {
                "id": self.left_player.id,
                "y": self.left_player.paddle.y_pos,
                "score": self.left_player.score,
            },
            "right_player": {
                "id": self.right_player.id,
                "y": self.right_player.paddle.y_pos,
                "score": self.right_player.score,
            },
        }

    def update(self):
        scored, player = self.ball.move(self.left_player, self.right_player)
        if scored:
            player.increment_score()
