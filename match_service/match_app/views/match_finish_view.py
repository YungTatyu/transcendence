from typing import Optional

from django.conf import settings
from django.utils.timezone import now
from match_app.client.tournament_client import TournamentClient
from match_app.models import Match, MatchParticipant
from match_app.serializers import MatchFinishSerializer
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from rest_framework.views import APIView


class MatchFinishView(APIView):
    """試合終了時のトーナメントAPIへの通知とDBレコードの更新"""

    def post(self, request):
        serializer = MatchFinishSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        match_id: int = serializer.validated_data["matchId"]
        results: list[dict] = serializer.validated_data["results"]
        match = Match.objects.filter(match_id=match_id).first()

        finish_date = self.update_match_data(match_id, results)
        if match.mode == "Tournament":
            self.register_winner_in_parent_match(match, results)
            err_message = self.send_match_result_to_tournament(match)
            if err_message is not None:
                self.rollback_match_data(match_id, match, results)
                return Response(
                    {"error": err_message}, status=HTTP_500_INTERNAL_SERVER_ERROR
                )

        return Response({"finishDate": str(finish_date)}, status=HTTP_200_OK)

    @staticmethod
    def update_match_data(match_id: int, results: list[dict]) -> now:
        # MatchParticipantのscoreをユーザーそれぞれに対して更新
        for result in results:
            user_id = result["userId"]
            score = result["score"]
            MatchParticipant.objects.filter(match_id=match_id, user_id=user_id).update(
                score=score
            )

        # Matchのwinner_user_idとfinish_dateを更新
        winner_user_id = max(results, key=lambda x: x["score"])["userId"]
        finish_date = now()
        Match.objects.filter(match_id=match_id).update(
            winner_user_id=winner_user_id, finish_date=finish_date
        )

        return finish_date

    @staticmethod
    def register_winner_in_parent_match(match: Match, results: list[dict]):
        parent_match = match.parent_match_id
        if parent_match is None:  # 親試合が無い == 決勝戦
            return

        winner_user_id = max(results, key=lambda x: x["score"])["userId"]
        MatchParticipant.objects.create(match_id=parent_match, user_id=winner_user_id)

    @staticmethod
    def rollback_match_data(match_id: int, match: Match, results: list[dict]):
        """
        __update_match_data と __register_winner_in_parent_matchのロールバックを実行
        """
        # MatchParticipantのスコアをリセット
        MatchParticipant.objects.filter(match_id=match_id).update(score=None)

        # Match の winner_user_id と finish_date をリセット
        Match.objects.filter(match_id=match_id).update(
            winner_user_id=None, finish_date=None
        )

        # 親試合が無い(決勝戦)場合、これ以降のロールバックは必要ない
        parent_match = match.parent_match_id
        if parent_match is None:
            return

        # 勝ち上がり処理で親試合に追加した試合参加者レコードを削除
        winner_user_id = max(results, key=lambda x: x["score"])["userId"]
        MatchParticipant.objects.filter(
            match_id=parent_match, user_id=winner_user_id
        ).delete()

    @staticmethod
    def send_match_result_to_tournament(match: Match) -> Optional[str]:
        """/tournaments/finish-matchを叩き、試合終了を通知"""
        client = TournamentClient(settings.TOURNAMENT_API_BASE_URL)
        response = client.finish_match(match.tournament_id, match.round)
        if response.status_code == 200:
            return None
        return "Internal Server Error"
