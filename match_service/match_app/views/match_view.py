from django.utils.decorators import method_decorator
from match_app.jwt_decorators import jwt_required
from match_app.models import Match, MatchParticipant
from match_app.serializers import MatchSerializer
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView


class MatchView(APIView):
    """QueryStringに指定された条件を用いてMatchを検索"""

    @method_decorator(jwt_required)
    def get(self, request):
        serializer = MatchSerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        filters = self.__create_filters(serializer.validated_data)
        matches: list[Match] = list(
            # 並び順を固定(offsetとlimitを使うため)
            Match.objects.filter(**filters).order_by("match_id")
        )

        offset = serializer.validated_data["offset"]
        limit = serializer.validated_data["limit"]

        # N+1によるパフォーマンス低下はoffset&limitで軽減できると考えています
        sliced_matches = matches[offset : offset + limit]
        results = [self.__convert_match_to_result(match) for match in sliced_matches]

        data = {
            "total": len(matches),
            "offset": offset,
            "limit": len(results),
            "results": results,
        }
        return Response(data=data, status=HTTP_200_OK)

    def __create_filters(self, validated_data: dict) -> dict:
        """複数条件でDBレコードを検索するための辞書を作成"""
        filters = {}
        # INFO Dict.get(key)はDict内にkeyが存在しない場合にNoneを返します
        if validated_data.get("matchId") is not None:
            filters["match_id"] = validated_data["matchId"]
        if validated_data.get("winnerUserId") is not None:
            filters["winner_user_id"] = validated_data["winnerUserId"]
        if validated_data.get("mode") is not None:
            filters["mode"] = validated_data["mode"]
        if validated_data.get("tournamentId") is not None:
            filters["tournament_id"] = validated_data["tournamentId"]
        if validated_data.get("round") is not None:
            filters["round"] = validated_data["round"]
        return filters

    def __convert_match_to_result(self, match: Match) -> dict:
        """MatchとMatchParticipantレコードをを用いて試合結果データを作成"""
        participants = MatchParticipant.objects.filter(match_id=match.match_id)
        participants_data = [
            {"id": participant.user_id, "score": participant.score}
            for participant in participants
        ]
        parent_match = match.parent_match_id
        parent_match_id = None if parent_match is None else parent_match.match_id

        result = {
            "matchId": match.match_id,
            "winnerUserId": match.winner_user_id,
            "mode": match.mode,
            "tournamentId": match.tournament_id,
            "parentMatchId": parent_match_id,
            "round": match.round,
            "participants": participants_data,
        }
        return result
