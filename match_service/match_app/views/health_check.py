from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK


@api_view(["GET"])
def health_check(_):
    return Response(data={"status": "healthy"}, status=HTTP_200_OK)
