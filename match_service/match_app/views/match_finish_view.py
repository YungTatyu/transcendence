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
