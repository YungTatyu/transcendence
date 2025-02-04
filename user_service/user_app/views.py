from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def health_check(request):
    """
    healthチェック
    user serverが機能している際は200を返す
    """
    return Response(data={"status": "healthy"}, status=status.HTTP_200_OK)
