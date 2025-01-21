from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User 

from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from .models import  User, AccessToken
from .serializers import RegisterSerializer,LoginSerializer, UserUpdateSerializer

# Create your views here.

class RegisterView(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        print(request.data)
        
        # シリアライザの初期化
        serializer = RegisterSerializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            # パスワードと確認パスワードの一致を確認
            password_confirmation = request.data.get('password_confirmation')
            if serializer.validated_data['password'] != password_confirmation:
                return Response(
                    {"error": 2, "message": "Passwords do not match"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # ユーザーIDの重複確認
            user_id = serializer.validated_data.get('user_id')
            if User.objects.filter(user_id=user_id).exists():
                return Response(
                    {"error": 3, "message": "User ID already exists"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # 新しいユーザーを保存
            try:
                user = serializer.save()
            except Exception as e:
                print(f"Database error: {e}")
                return Response(
                    {"error": 11, "message": "Database error occurred"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            # 成功時のレスポンス
            return Response(
                {"message": "User created successfully", "user": serializer.data},
                status=status.HTTP_201_CREATED
            )

        # シリアライザのエラーメッセージを返す
        return Response(
            {"error": serializer.errors, "message": "Invalid data"},
            status=status.HTTP_400_BAD_REQUEST
        )

class LoginView(GenericAPIView):
    """ログインAPIクラス"""
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = User.objects.get(user_id=serializer.validated_data["user_id"])
            user_id = serializer.validated_data['user_id']
            token = AccessToken.create(user)
            return Response({'detail': "ログインが成功しました。", 'error': 0, 'token': token.token, 'user_id': user_id})
        return Response({'error': 1}, status=HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):
    def get(self, request, user_id):
        # ユーザ情報の取得
        user = User.objects.filter(user_id=user_id).first()

        if not user:
            # ユーザが存在しない場合
            return Response({"message": "No User found"}, status=404)

        response_data = {
            "message": "User details by user_id",
            "user": {
                "user_id": user.user_id,
                "nickname": user.nickname,
                "comment": user.comment
            }
        }

        return Response(response_data, status=200)
    

class UserUpdateView(APIView):
    def patch(self, request, user_id):
        # ユーザ情報の取得
        user = User.objects.filter(user_id=user_id).first()

        if not user:
            # ユーザが存在しない場合
            return Response({"message": "No User found"}, status=404)

        if user_id != user.user_id:
            # 認証と異なるIDのユーザを指定した場合
            return Response({"message": "No Permission for Update"}, status=403)

        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            response_data = {
                "message": "User successfully updated",
                "user": {
                    "nickname": user.nickname,
                    "comment": user.comment
                }
            }
            return Response(response_data, status=200)
        else:
            error_message = serializer.errors.get('non_field_errors', ['User updation failed'])[0]
            return Response({"message": "User updation failed", "cause": error_message}, status=400)

    def post(self, request, user_id):
        return Response({"message": "Method not allowed"}, status=405)
    


class DeleteAccountView(APIView):
    def post(self, request,user_id):
        ## アカウントの削除処理
        try:
            user = User.objects.filter(user_id=user_id).first()
            user.delete()
        except User.DoesNotExist:
            raise Response("No User found")

        return Response({"message": "Account and user successfully removed"}, status=200)
        