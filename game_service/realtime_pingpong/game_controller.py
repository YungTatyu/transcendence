import asyncio

from core.pingpong import PingPong

from realtime_pingpong.consumers import GameConsumer


class GameContoroller:
    """
    game進行を管理する
    """

    def __init__(self):
        self.game = PingPong()
        self.__task = None

    def start_game(self, match_id):
        if self.__task is not None:
            raise RuntimeError("task alredy exists.")
        self.__task = asyncio.create_task(self.game_loop(match_id))

    def stop_game(self):
        if self.task is not None:
            self.task.cancel()
            self.task = None

    async def game_loop(self, match_id):
        try:
            while self.game.__state != PingPong.GameState.GAME_OVER:
                self.game.update()
                await GameConsumer.group_send(
                    {
                        "message": GameConsumer.MessageType.MSG_UPDATE.value,
                        "data": {
                            "state": self.game.get_state(),
                        },
                    },
                    match_id,
                )
                await asyncio.sleep(1 / 60)  # 60FPS (約16.67ミリ秒間隔)
        except asyncio.CancelledError:
            print("Game loop was cancelled.")
