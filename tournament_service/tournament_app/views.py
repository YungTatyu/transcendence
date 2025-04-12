from asgiref.sync import async_to_sync
from django.utils.decorators import method_decorator
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from rest_framework.views import APIView

from tournament_app.serializers import TournamentMatchFinishSerializer
from tournament_app.utils.apikey_decorators import apikey_required
from tournament_app.utils.tournament_session import TournamentSession


class TournamentMatchFinishView(APIView):
    """トーナメント試合終了時のroundの更新"""

    @method_decorator(apikey_required("tournaments"))
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

        async_to_sync(
            tournament_session.update_tournament_session_info,
            force_new_loop=False,
        )()
        return Response({"message": "Match ended normally"}, status=HTTP_200_OK)


@api_view(["GET"])
def health_check(_):
    return Response(data={"status": "healthy"}, status=HTTP_200_OK)
