import io
import logging

import jwt
import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.utils.timezone import now
from PIL import Image
from rest_framework import status
from rest_framework.test import APIClient

from user_app.models import User  # 正しい `User` モデルをインポート

logger = logging.getLogger(__name__)

SECRET_KEY = "test_secret"  # テスト用の秘密鍵
ALGORITHM = "HS256"


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_user(db):
    """テスト用のユーザーを作成"""
    user = User.objects.create(
        username="testuser",
        avatar_path=User.DEFAULT_AVATAR_PATH,
        created_at=now(),
    )

    # JWT トークンの作成
    token_payload = {"user_id": user.user_id}
    token = jwt.encode(token_payload, SECRET_KEY, algorithm=ALGORITHM)

    return user, token


@pytest.fixture
def create_another_user(db):
    """重複チェック用のユーザーを作成"""
    return User.objects.create(
        username="existuser",
        avatar_path=User.DEFAULT_AVATAR_PATH,
        created_at=now(),
    )


@pytest.fixture(autouse=True)
def setup_test(request, api_client, create_user):
    """各テスト実行前に API クライアントをセットアップ"""
    user, token = create_user

    logger.error(f"Generated token: {token}")
    assert token is not None, "JWT トークンが `None` になっています"

    api_client.cookies["access_token"] = token
    logger.error(f"Headers: {api_client._credentials}")

    request.cls.api_client = api_client
    request.cls.user, request.cls.token = create_user
    request.cls.api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {request.cls.token}")


@pytest.mark.usefixtures("setup_test")
@pytest.mark.django_db
class TestUsernameViewPut:
    def test_put_username_success(self):
        """PUT: 正常にユーザー名を変更 (成功)"""
        url = reverse("update-username")
        response = self.api_client.put(url, {"username": "new_name"}, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["username"] == "new_name"

    def test_put_username_validation_error_empty(self):
        """PUT: username が空の場合（バリデーションエラー）"""
        url = reverse("update-username")
        response = self.api_client.put(url, {"username": ""}, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "username" in response.data

    def test_put_username_already_taken(self, create_another_user):
        """PUT: すでに存在する username を指定した場合（重複エラー）"""
        url = reverse("update-username")
        response = self.api_client.put(url, {"username": "existuser"}, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.usefixtures("setup_test")
@pytest.mark.django_db
class TestAvatarViewPut:
    def test_put_avatar_success(self):
        """PUT: アバター画像を正常に更新"""

        url = reverse("update-avatar")

        # PIL でテスト用の画像を作成
        image_io = io.BytesIO()
        image = Image.new("RGB", (100, 100), "white")
        image.save(image_io, format="PNG")
        image_io.seek(0)

        # テスト用の画像ファイルを作成
        image_file = SimpleUploadedFile(
            "avatar.png", image_io.read(), content_type="image/png"
        )

        response = self.api_client.put(
            url, {"avatar_path": image_file}, format="multipart"
        )

        # DBをリロードして変更が適用されたか確認
        self.user.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert "avatarPath" in response.data

    def test_put_avatar_invalid_data(self):
        """PUT: 無効なデータを送信した場合(エラー)"""
        url = reverse("update-avatar")
        response = self.api_client.put(url, {"avatar_path": ""}, format="multipart")

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.usefixtures("setup_test")
@pytest.mark.django_db
class TestAvatarViewDelete:
    def test_delete_avatar_success(self):
        """DELETE: アバターを正常に削除（デフォルト画像にリセット）"""
        url = reverse("update-avatar")
        self.user.avatar_path = "images/uploads/custom_avatar.jpg"
        self.user.save()

        response = self.api_client.delete(url)
        self.user.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert self.user.avatar_path == User.DEFAULT_AVATAR_PATH  # デフォルト画像に戻る

    def test_delete_avatar_already_default(self):
        """DELETE: すでにデフォルトアバターの場合（エラー）"""
        url = reverse("update-avatar")
        response = self.api_client.delete(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
