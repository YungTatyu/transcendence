import json

from django.contrib.auth.hashers import make_password
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework.views import APIView

from auth_app.jwt_decorators import jwt_required
from auth_app.models import CustomUser
from auth_app.serializers.update_password_serializer import UpdatePasswordSerializer


class UpdatePasswordView(APIView):
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

            # 現在のユーザを取得
            try:
                user = CustomUser.objects.get(user_id=request.user_id)
            except CustomUser.DoesNotExist:
                return Response({"error": "User not found."}, status=404)

            serializer = UpdatePasswordSerializer(data=data, context={"user": user})

            try:
                serializer.is_valid(raise_exception=True)
            except Exception as e:
                return Response({"error": str(e)}, status=400)

            user.password = make_password(serializer.validated_data["new_password"])
            user.save()

            return Response({"message": "Password updated successfully."}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
