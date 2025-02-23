from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from rest_framework.views import APIView
import sys

from tournament_app.serializers import TournamentMatchFinishSerializer
from tournament_app.utils.tournament_session import TournamentSession
from asgiref.sync import async_to_sync


class TournamentMatchFinishView(APIView):
    """トーナメント試合終了時のroundの更新"""

    def post(self, request):
        serializer = TournamentMatchFinishSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        tournament_id = serializer.validated_data["tournamentId"]
        tournament_session = TournamentSession.search(tournament_id)
        if tournament_session is None:
            return Response(
                {"error": "Internal Server Error"},
                status=HTTP_500_INTERNAL_SERVER_ERROR,
            )

        async_to_sync(tournament_session.update_tournament_session_info())
        return Response({"message": "Match ended normally"}, status=HTTP_200_OK)


@api_view(["GET"])
def health_check(_):
    return Response(data={"status": "healthy"}, status=HTTP_200_OK)
