import json
import logging

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework.exceptions import APIException

from auth_app.jwt_decorators import jwt_required
from auth_app.models import CustomUser
from auth_app.serializers.update_email_serializer import UpdateEmailSerializer

logger = logging.getLogger(__name__)


class UpdateEmailView(View):
    """
    認証済みユーザの email を更新するエンドポイント
    """

    @method_decorator(jwt_required)
    def put(self, request):
        try:
            # JSONデータを取得
            data = json.loads(request.body)

            # 現在のユーザを取得
            try:
                user = CustomUser.objects.get(user_id=request.user_id)
            except CustomUser.DoesNotExist:
                return JsonResponse({"error": "User not found."}, status=404)

            try:
                serializer = UpdateEmailSerializer(
                    instance=user, data=data, context={"user": user}
                )
                serializer.is_valid(raise_exception=True)
            except APIException as e:
                return JsonResponse({"error": str(e)}, status=e.status_code)

            serializer.save()
            return JsonResponse({"message": "Email updated successfully."}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format."}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
