from rest_framework.views import APIView
from rest_framework.response import Response


class HealthCheckView(APIView):
    def get(self, _):
        return Response({"status": "healthy"})
