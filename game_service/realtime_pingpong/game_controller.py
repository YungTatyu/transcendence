import asyncio
from datetime import datetime, timedelta

from core.pingpong import PingPong


class GameContoroller:
    """
    game進行を管理する
    """

    GAME_TIME_SEC = 60

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
            end_time = await self.__announce_game_end_time(group_name)

            while not self.__is_game_over(end_time):
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

    def __calc_unix_time(self, time):
        return int(time.timestamp())

    async def __announce_game_end_time(self, group_name):
        from realtime_pingpong.consumers import GameConsumer

        end_time = self.__calc_unix_time(
            datetime.now() + timedelta(seconds=self.GAME_TIME_SEC)
        )
        await GameConsumer.group_send(
            {
                "message": GameConsumer.MessageType.MSG_TIMER.value,
                "end_time": end_time,
            },
            group_name,
        )
        return end_time

    def __is_game_over(self, end_time):
        return (
            self.__calc_unix_time(datetime.now()) >= end_time
            and self.game.is_match_over()
        )
