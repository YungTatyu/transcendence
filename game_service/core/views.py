from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class Games(APIView):
    def post(self, request):
        pass


@api_view(["GET"])
def health(request):
    return Response(data={"status": "healthy"}, status=status.HTTP_200_OK)
