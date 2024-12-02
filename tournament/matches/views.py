from django.db import Error
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Tournament, User, Match, MatchParticipant
from .serializers import TournamentDeserializer, TournamentSerializer, UserSerializer


class TournamentView(APIView):
    def post(self, request):
        serializer = TournamentDeserializer(data=request.data)
        if serializer.is_valid():
            players = serializer.validated_data['players']
            total_round = len(players) - 1

            # Create Tournament Record
            tournament = Tournament.objects.create(total_round=total_round)

            # Create Match Records
            match_list = []
            for i in range(1, total_round + 1):
                match = Match.objects.create(
                    mode="Tournament",
                    tournament_id=tournament.id,
                    parent_match_id=(None if i == 1 else match_list[int(i / 2) - 1].id),
                    round=(total_round - i + 1),
                )
                match_list.append(match)
                # print(match)

            # Create MatchPerticipant Records
            for i, player in enumerate(players):
                try:
                    user = User.objects.get(name=player)
                except Error:
                    print("指定されたユーザーが存在しません")
                    continue
                match_participant = MatchParticipant.objects.create(
                    match_id=match_list[total_round - 1 - int(i / 2)].id,
                    user_id = user.id
                )
                # print(match_participant)
            return Response({"tournament_id": tournament.id, "players": players}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, _, tournament_id):
        try:
            tournament = Tournament.objects.get(id=tournament_id)
        except ValueError:
            return Response({"detail": "Tournament not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = TournamentSerializer(tournament)
        return Response(serializer.data)


class UserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, _):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
