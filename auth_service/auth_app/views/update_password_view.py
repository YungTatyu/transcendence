import json

from django.contrib.auth.hashers import check_password, make_password
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View

from auth_app.jwt_decorators import jwt_required
from auth_app.models import CustomUser


class UpdatePasswordView(View):
    """
    認証済みユーザのパスワードを更新するエンドポイント
    """

    @method_decorator(jwt_required)
    def put(self, request):
        """
        ユーザのパスワードを更新する
        """
        try:
            # JSONデータを取得
            data = json.loads(request.body)
            current_password = data.get("current_password")
            new_password = data.get("new_password")

            if not current_password or not new_password:
                return JsonResponse(
                    {"error": "Both current and new passwords are required."},
                    status=400,
                )

            # 現在のユーザを取得
            user = CustomUser.objects.get(user_id=request.user_id)

            # 現在のパスワードの確認
            if not check_password(current_password, user.password):
                return JsonResponse(
                    {"error": "Current password is incorrect."}, status=400
                )

            # 新しいパスワードをハッシュ化して更新
            user.password = make_password(new_password)
            user.save()

            return JsonResponse(
                {"message": "Password updated successfully."}, status=200
            )

        except CustomUser.DoesNotExist:
            return JsonResponse({"error": "User not found."}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
