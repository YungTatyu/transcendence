import json

from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View

from auth_app.jwt_decorators import jwt_required
from auth_app.models import CustomUser


class UpdateEmailView(View):
    """
    認証済みユーザの email を更新するエンドポイント
    """

    @method_decorator(jwt_required)
    def put(self, request):
        """
        ユーザのメールアドレスを更新する
        """
        try:
            # JSONデータを取得
            data = json.loads(request.body)
            new_email = data.get("email")

            if not new_email:
                return JsonResponse({"error": "Email is required."}, status=400)

            # メールアドレスのバリデーション
            try:
                validate_email(new_email)
            except ValidationError:
                return JsonResponse({"error": "Invalid email format."}, status=400)

            # 現在のユーザを取得
            user = CustomUser.objects.get(user_id=request.user_id)

            # メールアドレスの重複チェック
            if (
                CustomUser.objects.filter(email=new_email)
                .exclude(user_id=user.user_id)
                .exists()
            ):
                return JsonResponse(
                    {"error": "This email address is already in use."}, status=409
                )

            # メールアドレスを更新
            user.email = new_email
            user.save()

            return JsonResponse({"message": "Email updated successfully."}, status=200)

        except CustomUser.DoesNotExist:
            return JsonResponse({"error": "User not found."}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
