import asyncio

from core.pingpong import PingPong


class GameContoroller:
    """
    game進行を管理する
    """

    def __init__(self):
        self.game = PingPong()
        self.__task = None

    def start_game(self, group_name):
        if self.__task is not None:
            raise RuntimeError("task alredy exists.")
        self.__task = asyncio.create_task(self.game_loop(group_name))

    def stop_game(self):
        if self.task is not None:
            self.task.cancel()
            self.task = None

    async def game_loop(self, group_name):
        # 遅延インポートで循環インポートを防ぐ
        from realtime_pingpong.consumers import GameConsumer

        try:
            while self.game.state != PingPong.GameState.GAME_OVER:
                self.game.update()
                await GameConsumer.group_send(
                    {
                        "message": GameConsumer.MessageType.MSG_UPDATE.value,
                        "data": {
                            "state": self.game.get_state(),
                        },
                    },
                    group_name,
                )
                await asyncio.sleep(1 / 60)  # 60FPS (約16.67ミリ秒間隔)
        except asyncio.CancelledError:
            print("Game loop was cancelled.")
