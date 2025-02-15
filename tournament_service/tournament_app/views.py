from rest_framework.decorators import api_view
from rest_framework.response import Response
from tournament_app.serializers import TournamentMatchFinishSerializer
from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from tournament_app.utils.tournament_session import TournamentSession


class TournamentMatchFinishView(APIView):
    """トーナメント試合終了時のroundの更新"""

    def post(self, request):
        serializer = TournamentMatchFinishSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        tournament_id = serializer.validated_data["tournamentId"]
        tournament_session = TournamentSession.search(tournament_id)
        self.__update_tournament_info(tournament_session)

        return Response({"message": "Match ended normally"}, status=HTTP_200_OK)

    def __update_tournament_info(self, tournament_session):
        """
        トーナメントの情報を更新し、次の試合のアナウンスメントイベントを発生させる
        TODO channel_layerに対して情報を伝達する処理
            (実現できるかわからないので、無理ならTournamentConsumerでポーリング)
        """
        tournament_session.next_round()


@api_view(["GET"])
def health_check(_):
    return Response(data={"status": "healthy"}, status=HTTP_200_OK)
