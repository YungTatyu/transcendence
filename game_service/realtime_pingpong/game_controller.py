import asyncio
from datetime import datetime, timedelta

from core.pingpong import PingPong


class PlayerManager:
    """プレイヤーの接続状態を管理する"""

    def __init__(self):
        self.players: dict[int, bool] = {}

    def add_players(self, players):
        self.players = {player: True for player in players}

    def reconnect_player(self, player_id):
        self.players[player_id] = True

    def disconnect_player(self, player_id):
        if player_id in self.players:
            self.players[player_id] = False

    def is_active(self, player_id):
        return self.players[player_id]

    def has_active_players(self):
        """
        アクティブなプレイヤーが存在するか
        """
        return any(self.players.values())


class GameController:
    """
    game進行を管理する
    """

    GAME_TIME_SEC = 60
    FRAME_DURATION = 1 / 60

    def __init__(self):
        self.__game = PingPong()
        self.__task = None
        self.__player_manager = PlayerManager()
        self.__game_end_time = 0

    @property
    def game(self):
        return self.__game

    def start_game(self, group_name):
        self.__player_manager.add_players(
            [self.__game.left_player.id, self.__game.right_player.id]
        )
        self.__game.state = PingPong.GameState.IN_PROGRESS
        self.__task = asyncio.create_task(self.game_loop(group_name))

    def stop_game(self):
        if self.__task is not None:
            self.__task.cancel()
            self.__task = None

    async def reconnect_event(self, group_name, player_id):
        self.__player_manager.reconnect_player(player_id)
        await self.__announce_game_end_time(group_name)

    def disconnect_event(self, player_id):
        self.__player_manager.disconnect_player(player_id)

    async def game_loop(self, group_name):
        # 遅延インポートで循環インポートを防ぐ
        from realtime_pingpong.consumers import GameConsumer

        try:
            self.__game_end_time = self.__calc_unix_time(
                datetime.now() + timedelta(seconds=self.GAME_TIME_SEC)
            )
            await self.__announce_game_end_time(group_name)

            while not self.__is_game_over(self.__game_end_time):
                self.__game.update()
                await GameConsumer.group_send(
                    {
                        "message": GameConsumer.MessageType.MSG_UPDATE,
                        "data": {
                            "state": self.__game.get_state(),
                        },
                    },
                    group_name,
                )
                await asyncio.sleep(self.FRAME_DURATION)
            self.__game.state = PingPong.GameState.GAME_OVER
            GameConsumer.finish_game({}, group_name)
        except asyncio.CancelledError:
            pass

    def __calc_unix_time(self, time):
        return int(time.timestamp())

    async def __announce_game_end_time(self, group_name):
        from realtime_pingpong.consumers import GameConsumer

        await GameConsumer.group_send(
            {
                "message": GameConsumer.MessageType.MSG_TIMER.value,
                "end_time": self.__game_end_time,
            },
            group_name,
        )

    def __is_game_over(self, end_time):
        return (
            self.__calc_unix_time(datetime.now()) >= end_time
            and self.__game.is_match_over()
        )
