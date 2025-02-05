import json
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from auth_app.jwt_decorators import jwt_required
from auth_app.models import CustomUser
from auth_app.serializers.update_email_serializer import UpdateEmailSerializer


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

            # シリアライザでバリデーション & 更新
            serializer = UpdateEmailSerializer(instance=user, data=data, context={"user": user})
            if not serializer.is_valid():
                return JsonResponse({"error": serializer.errors}, status=400)

            serializer.save()
            return JsonResponse({"message": "Email updated successfully."}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format."}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
