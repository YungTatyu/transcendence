import io
from unittest.mock import patch

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from PIL import Image
from rest_framework import status
from rest_framework.test import APIClient

from ..models import User


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_user():
    """テスト用のユーザーを作成する"""
    return User.objects.create(user_id=1, username="testuser")


@pytest.fixture
def create_another_user():
    """すでに存在する別のユーザーを作成（重複チェック用）"""
    return User.objects.create(user_id=2, username="existuser")


@pytest.mark.django_db
class TestUsernameViewPut:
    def test_put_username_success(self, api_client, create_user):
        """PUT: 正常にユーザー名を変更 (成功)"""
        response = api_client.put(
            reverse("update-username"), {"username": "new_name"}, format="json"
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["username"] == "new_name"

    def test_put_username_user_not_found(self, api_client):
        """PUT: ユーザーが存在しない場合(エラー)"""
        response = api_client.put(
            reverse("update-username"), {"username": "nonuser"}, format="json"
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["error"] == "User not found"

    def test_put_username_validation_error_empty(self, api_client, create_user):
        """PUT: username が空の場合（バリデーションエラー）"""
        response = api_client.put(
            reverse("update-username"), {"username": ""}, format="json"
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "username" in response.data

    def test_put_username_validation_error_too_long(self, api_client, create_user):
        """PUT: username が長すぎる場合（バリデーションエラー）"""
        response = api_client.put(
            reverse("update-username"), {"username": "longerusername"}, format="json"
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "username" in response.data

    def test_put_username_already_taken(
        self, api_client, create_user, create_another_user
    ):
        """PUT: すでに存在する username を指定した場合（重複エラー）"""
        response = api_client.put(
            reverse("update-username"), {"username": "existuser"}, format="json"
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestAvatarViewPut:
    def test_put_avatar_success(self, api_client, create_user):
        """PUT: defaultから正常にアバターを更新"""

        print("Before PUT:", create_user.avatar_path)
        # PIL でテスト用の画像を作成
        image_io = io.BytesIO()
        image = Image.new("RGB", (100, 100), "white")  # 100x100 の白い画像
        image.save(image_io, format="PNG")
        image_io.seek(0)

        # テスト用の画像ファイルを作成
        image_file = SimpleUploadedFile(
            "avatar.png", image_io.read(), content_type="image/png"
        )

        response = api_client.put(
            reverse("update-avatar"), {"avatar_path": image_file}, format="multipart"
        )

        # PUT後の avatar_path を再取得して確認
        create_user.refresh_from_db()  # DBの変更を反映
        print("After PUT:", create_user.avatar_path)

        assert response.status_code == status.HTTP_200_OK
        assert "avatarPath" in response.data

    def test_put_avatar_user_not_found(self, api_client):
        """PUT: ユーザーが存在しない場合(エラー)"""
        response = api_client.put(
            reverse("update-avatar"),
            {"avatar_path": "new_avatar.jpg"},
            format="multipart",
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["error"] == "User not found."

    def test_put_avatar_invalid_data(self, api_client, create_user):
        """PUT: 無効なデータを送信した場合(エラー)"""
        response = api_client.put(
            reverse("update-avatar"), {"avatar_path": ""}, format="multipart"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestAvatarViewDelete:
    @patch("os.path.exists", return_value=True)
    @patch("django.core.files.storage.default_storage.delete")
    def test_delete_avatar_success(
        self, mock_delete, mock_exists, api_client, create_user
    ):
        """DELETE: 正常にアバターを削除(成功)"""
        # ユーザーのアバターをカスタム画像に設定
        create_user.avatar_path = "avatars/custom_avatar.jpg"
        create_user.save()

        response = api_client.delete(reverse("update-avatar"))
        assert response.status_code == status.HTTP_200_OK
        mock_delete.assert_called_once()

    def test_delete_avatar_user_not_found(self, api_client):
        """DELETE: ユーザーが存在しない場合(エラー)"""
        response = api_client.delete(reverse("update-avatar"))
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["error"] == "User not found."

    def test_delete_avatar_already_default(self, api_client, create_user):
        """DELETE: すでにデフォルトアバターの場合(エラー)"""
        create_user.avatar_path = User.DEFAULT_AVATAR_PATH
        create_user.save()

        response = api_client.delete(reverse("update-avatar"))
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["error"] == "Avatar is default."
