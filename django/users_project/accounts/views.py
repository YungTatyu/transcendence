from django.shortcuts import render
from django.contrib.auth.models import User 
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from .models import  User, AccessToken
from .serializers import RegisterSerializer,LoginSerializer, UpdateUsernameSerializer


class RegisterView(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        print(request.data)
        
        # シリアライザの初期化
        serializer = RegisterSerializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            # # パスワードと確認パスワードの一致を確認
            # password_confirmation = request.data.get('password_confirmation')
            # if serializer.validated_data['password'] != password_confirmation:
            #     return Response(
            #         {"error": 2, "message": "Passwords do not match"},
            #         status=status.HTTP_400_BAD_REQUEST
            #     )

            # ユーザーIDの重複確認
            username = serializer.validated_data.get('username')
            if User.objects.filter(username=username).exists():
                return Response(
                    {"error": 3, "message": "User name already exists"},
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

            user = serializer.validated_data['user']  # `LoginSerializer` が認証済みユーザーを返す
            
            try:
                token = AccessToken.create(user)
            except Exception as e:
                return Response({'error': 1, 'detail': f'トークン生成エラー: {str(e)}'}, status=HTTP_500_INTERNAL_SERVER_ERROR)
            
            return Response({
                'detail': "ログインが成功しました。",
                'error': 0,
                'token': token.token,
                'username': user.username,
            })
        return Response({'error': 1}, status=HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):
    def get(self, request, username):
        # ユーザ情報の取得
        user = get_object_or_404(User, username=username)

        response_data = {
            "message": "User details by username",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            }
        }

        return Response(response_data, status=status.HTTP_200_OK)
    

class UpdateUsernameView(APIView):
    # permission_classes = [AllowAny]

    def patch(self, request, username):
        # ユーザ情報の取得
        user = get_object_or_404(User, username=username)

        if request.user.id != user.id:
            # 認証と異なるIDのユーザを指定した場合
            return Response({"message": "No Permission for Update"}, status=403)

        serializer = UpdateUsernameSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            updated_user = serializer.save()

            response_data = {
                "message": "User successfully updated",
                "user": {
                    "username": updated_user.username,  # 更新された username をレスポンスに含める
                }
            }
            return Response(response_data, status=200)
        else:
            return Response({
                "message": "User update failed",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, user_id):
        return Response({"message": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class DeleteAccountView(APIView):
    def post(self, request,user_id):
        ## アカウントの削除処理
        try:
            user = User.objects.filter(id=user_id).first()
            user.delete()
        except User.DoesNotExist:
            raise Response("No User found")

        return Response({"message": "Account and user successfully removed"}, status=200)
        