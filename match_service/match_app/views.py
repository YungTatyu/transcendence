from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view


class MatchView(APIView):
    def get(self, request):
        pass


class TournamentMatchView(APIView):
    def post(self, request):
        pass


class MatchFinishView(APIView):
    def post(self, request):
        pass


class MatchStatisticView(APIView):
    def get(self, request):
        pass


class MatchHistoryView(APIView):
    def get(self, request):
        pass


@api_view(["GET"])
def health_check(_):
    return Response(data={"status": "healthy"}, status=status.HTTP_200_OK)
