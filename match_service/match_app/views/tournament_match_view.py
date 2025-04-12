from typing import Optional

from django.utils.decorators import method_decorator
from match_app.models import Match, MatchParticipant
from match_app.serializers import TournamentMatchSerializer
from match_app.utils.apikey_decorators import apikey_required
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView


class TournamentMatchView(APIView):
    """トーナメント試合レコードを作成"""

    @method_decorator(apikey_required("matches"))
    def post(self, request):
        serializer = TournamentMatchSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        parent_match_id: Optional[int] = serializer.validated_data["parentMatchId"]
        parent_match = Match.objects.filter(match_id=parent_match_id).first()

        # Matchレコードの作成
        tournament_match = Match.objects.create(
            mode="Tournament",
            start_date=None,
            tournament_id=serializer.validated_data["tournamentId"],
            parent_match_id=parent_match,
            round=serializer.validated_data["round"],
        )

        # MatchParticipantレコードの作成
        for user_id in serializer.validated_data["userIdList"]:
            MatchParticipant.objects.create(match_id=tournament_match, user_id=user_id)

        return Response(data={"matchId": tournament_match.match_id}, status=HTTP_200_OK)
