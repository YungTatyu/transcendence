from match_app.models import Match, MatchParticipant
from match_app.serializers import UserIdValidator
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView


class MatchStatisticView(APIView):
    """user_idに対応する統計情報を取得する"""

    def get(self, _, user_id):
        user_id_validator = UserIdValidator(data={"user_id": user_id})
        if not user_id_validator.is_valid():
            return Response(user_id_validator.errors, status=HTTP_400_BAD_REQUEST)

        user_id = int(user_id_validator.validated_data["user_id"])

        data = {
            "matchWinCount": self.__fetch_match_win_count(user_id),
            "matchLoseCount": self.__fetch_match_lose_count(user_id),
            "tournamentWinnerCount": self.__fetch_tournament_winner_count(user_id),
        }
        return Response(data=data, status=HTTP_200_OK)

    def __fetch_match_win_count(self, user_id: int) -> int:
        match_win_count = Match.objects.filter(winner_user_id=user_id).count()
        return match_win_count

    def __fetch_match_lose_count(self, user_id: int) -> int:
        lose_matches_count = (
            MatchParticipant.objects.filter(
                user_id=user_id,  # 試合参加者である
                match_id__finish_date__isnull=False,  # 試合が終了している
            )
            .exclude(match_id__winner_user_id=user_id)  # 勝利した試合は除外
            .count()
        )
        return lose_matches_count

    def __fetch_tournament_winner_count(self, user_id: int) -> int:
        tournament_win_count = Match.objects.filter(
            finish_date__isnull=False,  # 試合が終了している
            mode="Tournament",  # トーナメントの試合である
            winner_user_id=user_id,  # `勝者である
            parent_match_id__isnull=True,  # 親試合がない == 決勝戦
        ).count()
        return tournament_win_count
