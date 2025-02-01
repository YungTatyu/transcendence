from typing import Optional

import requests
from django.utils.timezone import now
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from match_app.models import Matches, MatchParticipants
from match_app.serializers import (
    MatchesSerializer,
    MatchFinishSerializer,
    MatchHistorySerializer,
    TournamentMatchSerializer,
    UserIdValidator,
)


class MatchView(APIView):
    """QueryStringに指定された条件を用いてMatchesを検索"""

    def get(self, request):
        serializer = MatchesSerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        filters = self.__create_filters(serializer.validated_data)
        matches: list[Matches] = list(
            # 並び順を固定(offsetとlimitを使うため)
            Matches.objects.filter(**filters).order_by("match_id")
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

    def __convert_match_to_result(self, match: Matches) -> dict:
        """MatchesとMatchParticipantsレコードをを用いて試合結果データを作成"""
        participants = MatchParticipants.objects.filter(match_id=match.match_id)
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


class TournamentMatchView(APIView):
    """トーナメント試合レコードを作成"""

    def post(self, request):
        serializer = TournamentMatchSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        parent_match_id: Optional[int] = serializer.validated_data["parentMatchId"]
        parent_match = Matches.objects.filter(match_id=parent_match_id).first()

        # Matchesレコードの作成
        tournament_match = Matches.objects.create(
            mode="Tournament",
            tournament_id=serializer.validated_data["tournamentId"],
            parent_match_id=parent_match,
            round=serializer.validated_data["round"],
        )

        # MatchParticipantsレコードの作成
        for user_id in serializer.validated_data["userIdList"]:
            MatchParticipants.objects.create(match_id=tournament_match, user_id=user_id)

        return Response(data={"matchId": tournament_match.match_id}, status=HTTP_200_OK)


class MatchFinishView(APIView):
    """試合終了時のトーナメントAPIへの通知とDBレコードの更新"""

    def post(self, request):
        serializer = MatchFinishSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        match_id: int = serializer.validated_data["matchId"]
        results: list[dict] = serializer.validated_data["results"]

        # 先にトーナメントAPIを叩く(整合性維持のため)
        if not self.__send_match_result_if_tournament_match(match_id):
            return Response(
                {"error": "Tournament API was not consistent"},
                status=HTTP_400_BAD_REQUEST,
            )

        finish_date = self.__update_match_data(match_id, results)
        return Response({"finishDate": str(finish_date)}, status=HTTP_200_OK)

    def __update_match_data(self, match_id: int, results: list[dict]) -> now:
        # MatchParticipantsのscoreをユーザーそれぞれに対して更新
        for result in results:
            user_id = result["userId"]
            score = result["score"]
            MatchParticipants.objects.filter(match_id=match_id, user_id=user_id).update(
                score=score
            )

        # Matchesのwinner_user_idとfinish_dateを更新
        winner_user_id = max(results, key=lambda x: x["score"])["userId"]
        finish_date = now()
        Matches.objects.filter(match_id=match_id).update(
            winner_user_id=winner_user_id, finish_date=finish_date
        )

        return finish_date

    def __send_match_result_if_tournament_match(self, match_id: int) -> bool:
        """
        if (mode == Tournament):
            /tournaments/finish-matchを叩き、試合終了を通知
        else:
            何もしない
        """
        match = Matches.objects.filter(match_id=match_id).first()
        # modeがTournament以外なら何もしない
        if match.mode != "Tournament":
            return True

        url = f"{settings.TOURNAMENT_API_BASE_URL}/tournaments/finish-match"
        payload = {"tournamentId": match.tournament_id, "round": match.round}
        response = requests.post(url, json=payload)
        return response.status_code == 200


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

    def __fetch_tournament_winner_count(self, user_id: int) -> int:
        tournament_win_count = Matches.objects.filter(
            finish_date__isnull=False,  # 試合が終了している
            mode="Tournament",  # トーナメントの試合である
            winner_user_id=user_id,  # `勝者である
            parent_match_id__isnull=True,  # 親試合がない == 決勝戦
        ).count()
        return tournament_win_count


class MatchHistoryView(APIView):
    """user_idに対応する試合履歴情報を取得する"""

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

    def __fetch_finished_matches(self, user_id: int) -> list[Matches]:
        """特定のユーザーが参加し、試合が終了している試合を並び順を固定して取得"""
        finished_matches = (
            MatchParticipants.objects.filter(
                user_id=user_id,  # 試合参加者である
                match_id__finish_date__isnull=False,  # 終了した試合である
            )
            .select_related("match_id")  # 逆参照
            .order_by("match_id")  # 並び順を固定(offsetとlimitを使うため)
        )
        return [participant.match_id for participant in finished_matches]

    def __convert_match_to_result(self, match: Matches, user_id: int) -> dict:
        """MatchesとMatchParticipantsレコードをを用いて試合履歴データを作成"""
        win_or_lose = "win" if match.winner_user_id == user_id else "lose"
        participants = MatchParticipants.objects.filter(match_id=match.match_id)
        user = participants.filter(user_id=user_id).first()
        opponents = participants.exclude(user_id=user_id)
        opponents_data = [
            {"id": opponent.user_id, "score": opponent.score} for opponent in opponents
        ]

        result = {
            "mode": match.mode,
            "result": win_or_lose,
            "date": match.start_date,
            "userScore": user.score,
            "opponents": opponents_data,
        }
        return result


@api_view(["GET"])
def health_check(_):
    return Response(data={"status": "healthy"}, status=HTTP_200_OK)
