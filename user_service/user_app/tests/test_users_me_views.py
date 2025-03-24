import io

import jwt
import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.utils.timezone import now
from PIL import Image
from rest_framework import status
from rest_framework.test import APIClient

from user_app.models import User
from user_app.serializers import AvatarSerializer

SECRET_KEY = "test_secret"  # テスト用の秘密鍵
ALGORITHM = "HS256"


@pytest.fixture(scope="function")
def create_another_user(db):
    """重複チェック用のユーザーを作成"""
    return User.objects.create(
        username="existuser",
        avatar_path=User.DEFAULT_AVATAR_PATH,
        created_at=now(),
    )


@pytest.fixture
def setup_test(db, request):
    """各テスト実行前に API クライアントをセットアップ"""

    # ユーザー作成
    user = User.objects.create(
        username="testuser",
        avatar_path=User.DEFAULT_AVATAR_PATH,
    )

    # JWT トークンの作成（Cookieに設定するだけ）
    token_payload = {"user_id": user.user_id}
    token = jwt.encode(token_payload, SECRET_KEY, algorithm=ALGORITHM)

    api_client = APIClient()
    api_client.cookies["access_token"] = token  # Cookie に JWT をセット

    # クラス属性にセット（テストクラスで `self.api_client` を利用可能にする）
    if hasattr(request, "cls"):
        request.cls.api_client = api_client
        request.cls.user = user
        request.cls.token = token

    yield api_client, user, token


@pytest.mark.usefixtures("setup_test")
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
        assert response.data["error"] == "Invalid input."

    def test_put_username_validation_longer(self):
        """PUT: username が10文字以上の場合(バリデーションエラー)"""
        url = reverse("update-username")
        response = self.api_client.put(
            url, {"username": "longerusername"}, format="json"
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["error"] == "Invalid input."

    def test_put_username_already_taken(self, create_another_user):
        """PUT: すでに存在する username を指定した場合（重複エラー）"""
        url = reverse("update-username")
        response = self.api_client.put(url, {"username": "existuser"}, format="json")

        assert response.status_code == status.HTTP_409_CONFLICT
        assert response.data["error"] == "A username is already used."



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
        assert response.data["error"] == "Invalid image format."


    def test_put_avatar_oversized(self):
        """PUT: 4MBを超える画像ファイルをアップロード (エラー)"""

        url = reverse("update-avatar")

        # PIL で 3000x3000px の画像を作成
        image_io = io.BytesIO()
        image = Image.new("RGB", (3000, 3000), "white")
        image.save(image_io, format="PNG")
        image_io.seek(0)

        # 画像サイズが 4MB を超えるようにダミーデータを追加
        while image_io.tell() < (AvatarSerializer.MAX_FILE_SIZE) + 1:  # 4MB + 1B
            image_io.write(b"\0")  # 無意味なバイトを書き足す
        image_io.seek(0)

        # テスト用の画像ファイルを作成
        image_file = SimpleUploadedFile(
            "oversized_avatar.png", image_io.read(), content_type="image/png"
        )

        response = self.api_client.put(
            url, {"avatar_path": image_file}, format="multipart"
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["error"] == "Invalid image format."

