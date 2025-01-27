from typing import Optional
from django.utils.timezone import now
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .serializers import (
    TournamentMatchSerializer,
    MatchHistorySerializer,
    MatchFinishSerializer,
    MatchesSerializer,
)
from .models import Matches, MatchParticipants


class MatchView(APIView):
    def get(self, request):
        serializer = MatchesSerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        filters = self.__create_filters(serializer.validated_data)
        matches = list(Matches.objects.filter(**filters))

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
        return Response(data=data, status=status.HTTP_200_OK)

    def __create_filters(self, validated_data) -> dict:
        filters = {}
        if validated_data.get("matchId", None) is not None:
            filters["match_id"] = validated_data["matchId"]
        if validated_data.get("winnerUserId", None) is not None:
            filters["winner_user_id"] = validated_data["winnerUserId"]
        if validated_data.get("mode", None) is not None:
            filters["mode"] = validated_data["mode"]
        if validated_data.get("tournamentId", None) is not None:
            filters["tournament_id"] = validated_data["tournamentId"]
        if validated_data.get("round", None) is not None:
            filters["round"] = validated_data["round"]
        return filters

    def __convert_match_to_result(self, match: Matches) -> dict:
        participants = MatchParticipants.objects.filter(match_id=match.match_id)
        participant_data = [
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
            "participants": participant_data,
        }
        return result


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
        serializer = MatchFinishSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        match_id = serializer.validated_data["matchId"]
        results = serializer.validated_data["results"]
        if not self.__check_match_integrity(match_id, results):
            return Response(
                {"error": "The match data has integrity issues."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        finish_date = self.__update_match_data(match_id, results)

        self.__send_match_result_to_tournament_api(match_id)

        return Response({"finishDate": str(finish_date)}, status=status.HTTP_200_OK)

    def __check_match_integrity(self, match_id: int, results: list[dict]) -> bool:
        match = Matches.objects.filter(match_id=match_id).first()

        # 試合が存在しない
        if match is None:
            return False

        # 試合は既に終了している
        if match.finish_date is not None:
            return False

        # 勝者が複数存在する
        scores = [result["score"] for result in results]
        winner_score = max(scores)
        if scores.count(winner_score) != 1:
            return False

        # リクエストボディとDB内のuser_idsに整合性が無い
        user_ids = [result["userId"] for result in results]
        participants_ids = MatchParticipants.objects.filter(
            match_id=match_id
        ).values_list("user_id", flat=True)
        return set(user_ids) == set(participants_ids)

    def __update_match_data(self, match_id: int, results: list[dict]) -> now:
        for result in results:
            user_id = result["user_id"]
            score = result["score"]
            MatchParticipants.objects.filter(match_id=match_id, user_id=user_id).update(
                score=score
            )

        winner_user_id = max(results, key=lambda x: x["score"])
        finish_date = now()
        Matches.objects.filter(match_id=match_id).update(
            winner_user_id=winner_user_id, finish_date=finish_date
        )

        return finish_date

    def __send_match_result_to_tournament_api(self, match_id: int):
        """
        /tournaments/finish-match エンドポイントを叩き、TournamentAPIに試合が終了したことを通知
        """
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
    def get(self, request, user_id):
        serializer = MatchHistorySerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(
                {"error": "Bad QueryString"}, status=status.HTTP_400_BAD_REQUEST
            )

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
        return Response(data=data, status=status.HTTP_200_OK)

    def __fetch_finished_matches(self, user_id: int) -> list[Matches]:
        finished_matches = (
            MatchParticipants.objects.filter(
                user_id=user_id,  # 指定したuser_idを持つ参加者である
                match_id__finish_date__isnull=False,  # 終了した試合である
            )
            .select_related("match_id")  # 逆参照
            .order_by("match_id")  # 並び順を固定(offsetとlimitを使うため)
        )
        return [participant.match_id for participant in finished_matches]

    def __convert_match_to_result(self, match: Matches, user_id: int) -> dict:
        win_or_lose = "win" if match.winner_user_id == user_id else "lose"
        participants = MatchParticipants.objects.filter(match_id=match.match_id)
        user = participants.filter(user_id=user_id).first()
        opponents = participants.exclude(user_id=user_id)
        opponent_data = [
            {"id": opponent.user_id, "score": opponent.score} for opponent in opponents
        ]

        result = {
            "mode": match.mode,
            "result": win_or_lose,
            "date": match.start_date,
            "userScore": user.score,
            "opponents": opponent_data,
        }
        return result


@api_view(["GET"])
def health_check(_):
    return Response(data={"status": "healthy"}, status=status.HTTP_200_OK)
