from typing import Optional
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .serializers import TournamentMatchSerializer
from .models import Matches, MatchParticipants


class MatchView(APIView):
    def get(self, request):
        pass


class TournamentMatchView(APIView):
    """トーナメント試合レコードを作成"""

    def post(self, request):
        serializer = TournamentMatchSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        parent_match_id = serializer.validated_data["parentMatchId"]
        parent_match, is_err = self.__fetch_parent_match(parent_match_id)

        if is_err:
            return Response(
                {"error": "Parent match not found"}, status=status.HTTP_400_BAD_REQUEST
            )

        tournament_match = Matches.objects.create(
            mode="Tournament",
            tournament_id=serializer.validated_data["tournamentId"],
            parent_match_id=parent_match,
            round=serializer.validated_data["round"],
        )

        for user_id in serializer.validated_data["userIdList"]:
            MatchParticipants.objects.create(match_id=tournament_match, user_id=user_id)

        return Response(
            data={"matchId": tournament_match.match_id}, status=status.HTTP_200_OK
        )

    def __fetch_parent_match(
        self, parent_match_id: Optional[int]
    ) -> tuple[Optional[Matches], bool]:
        if parent_match_id is None:
            return (None, False)

        try:
            parent_match = Matches.objects.get(match_id=parent_match_id)
            return (parent_match, False)
        except Matches.DoesNotExist:
            return (None, True)


class MatchFinishView(APIView):
    def post(self, request):
        pass


class MatchStatisticView(APIView):
    def get(self, _, user_id):
        data = {
            "matchWinCount": self.__fetch_match_win_count(user_id),
            "matchLoseCount": self.__fetch_match_lose_count(user_id),
            "tournamentWinCount": self.__fetch_tournament_win_count(user_id),
        }
        return Response(data=data, status=status.HTTP_200_OK)

    def __fetch_match_win_count(self, user_id: int) -> int:
        match_win_count = Matches.objects.filter(winner_user_id=user_id).count()
        return match_win_count

    def __fetch_match_lose_count(self, user_id: int) -> int:
        lose_matches_count = (
            MatchParticipants.objects.filter(
                user_id=user_id,  # 試合参加者である
                match_id__finish_date__isnull=False,  # 試合が終了している
            )
            .exclude(match_id__winner_user_id=user_id)  # 勝利した試合は除外
            .count()
        )
        return lose_matches_count

    def __fetch_tournament_win_count(self, user_id: int) -> int:
        tournament_win_count = Matches.objects.filter(
            finish_date__isnull=False,  # 試合が終了している
            mode="Tournament",  # トーナメントの試合である
            winner_user_id=user_id,  # `勝者である
            parent_match_id__isnull=True,  # 親試合がない == 決勝戦
        ).count()
        return tournament_win_count


class MatchHistoryView(APIView):
    def get(self, request):
        pass


@api_view(["GET"])
def health_check(_):
    return Response(data={"status": "healthy"}, status=status.HTTP_200_OK)
