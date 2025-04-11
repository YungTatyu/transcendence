from django.utils.decorators import method_decorator
from match_app.jwt_decorators import jwt_required
from match_app.models import Match, MatchParticipant
from match_app.serializers import MatchHistorySerializer, UserIdValidator
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView


class MatchHistoryView(APIView):
    """user_idに対応する試合履歴情報を取得する"""

    @method_decorator(jwt_required)
    def get(self, request, user_id):
        serializer = MatchHistorySerializer(data=request.query_params)
        user_id_validator = UserIdValidator(data={"user_id": user_id})
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        elif not user_id_validator.is_valid():
            return Response(user_id_validator.errors, status=HTTP_400_BAD_REQUEST)

        user_id = int(user_id_validator.validated_data["user_id"])
        matches = self.__fetch_finished_matches(user_id)

        offset = serializer.validated_data["offset"]
        limit = serializer.validated_data["limit"]

        # N+1によるパフォーマンス低下はoffset&limitで軽減できると考えています
        sliced_matches = matches[offset : offset + limit]
        results = [
            self.__convert_match_to_result(match, user_id) for match in sliced_matches
        ]

        data = {
            "total": len(matches),
            "offset": offset,
            "limit": len(results),
            "results": results,
        }
        return Response(data=data, status=HTTP_200_OK)

    def __fetch_finished_matches(self, user_id: int) -> list[Match]:
        """特定のユーザーが参加し、試合が終了している試合を並び順を固定して取得"""
        finished_matches = (
            MatchParticipant.objects.filter(
                user_id=user_id,  # 試合参加者である
                match_id__finish_date__isnull=False,  # 終了した試合である
            )
            .select_related("match_id")  # 逆参照
            .order_by("match_id")  # 並び順を固定(offsetとlimitを使うため)
        )
        return [participant.match_id for participant in finished_matches]

    def __convert_match_to_result(self, match: Match, user_id: int) -> dict:
        """MatchとMatchParticipantレコードをを用いて試合履歴データを作成"""
        win_or_lose = "win" if match.winner_user_id == user_id else "lose"
        participants = MatchParticipant.objects.filter(match_id=match.match_id)
        user = participants.filter(user_id=user_id).first()
        opponents = participants.exclude(user_id=user_id)
        opponents_data = [
            {"id": opponent.user_id, "score": opponent.score} for opponent in opponents
        ]

        result = {
            "mode": match.mode,
            "result": win_or_lose,
            "date": match.finish_date,
            "userScore": user.score,
            "opponents": opponents_data,
        }
        return result
