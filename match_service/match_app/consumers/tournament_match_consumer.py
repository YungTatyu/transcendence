from channels.generic.websocket import AsyncWebsocketConsumer
from match_app.models import Match, MatchParticipant
from channels.db import database_sync_to_async


class TournamentMatchConsumer(AsyncWebsocketConsumer):
    GROUP_NAME_FORMAT = "match_{}"

    @classmethod
    def get_group_name(cls, match_id: int):
        # 定数をフォーマットして使用
        return cls.GROUP_NAME_FORMAT.format(match_id)

    async def connect(self):
        self.user_id = self.scope.get("user_id")
        if not self.user_id:
            await self.close()
            return

        self.match_id = int(self.scope["url_route"]["kwargs"]["matchId"])
        self.room_group_name = TournamentMatchConsumer.get_group_name(self.match_id)

        participant_ids = self.__select_match_participant_ids(self.match_id)
        if self.user_id not in participant_ids:
            await self.close(code=4400)
            return

        # WebSocket グループに参加
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        pass

    async def disconnect(self, _):
        pass

    @database_sync_to_async
    def __select_match_participant_ids(self, match_id: int) -> list[int]:
        match = Match.objects.filter(match_id=match_id)

        if (
            not match  # 試合が存在しない
            or match.finish_date is not None  # 試合が既に終了している
            or match.mode != "Tournament"  # 試合がTournamentの試合ではない
        ):
            return []

        curr_round = match.round
        # 初回のroundではない場合、一つ前のroundが終了しているかを確認
        if curr_round != 1:
            prev_round = curr_round - 1
            prev_match = Match.objects.filter(match_id=match_id, round=prev_round)
            if prev_match.finish_date is None:
                return []

        participant_ids = []
        for participant in MatchParticipant.objects.filter(match_id=match):
            participant_ids.append(participant.user_id)
        return participant_ids
