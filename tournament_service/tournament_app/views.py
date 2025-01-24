from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def health_check(_):
    return Response(data={"status": "healthy"}, status=status.HTTP_200_OK)
