import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from user_app.settings import CA_CERT, CLIENT_CERT, CLIENT_KEY, VAULT_ADDR
from user_app.vault_client.vault_client import VaultClient

from ..models import User


@pytest.fixture
def api_client():
    client = VaultClient(VAULT_ADDR, CLIENT_CERT, CLIENT_KEY, CA_CERT)
    token = client.fetch_token()
    api_keys = client.fetch_api_key(token, "users")
    api_client = APIClient()
    api_client.credentials(HTTP_X_API_KEY=api_keys["value"])
    return api_client


@pytest.fixture
def create_user():
    """テスト用のユーザーを作成する"""
    return User.objects.create(username="testuser")


@pytest.mark.django_db
class TestUserViewPost:
    def test_post_validation_error_no_username(self, api_client):
        """POST: バリデーションエラー(usernameなし)"""
        response = api_client.post(reverse("users"), data={})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "error" in response.data

    def test_post_validation_error_longerusernme(self, api_client):
        """POST: バリデーションエラー(username10文字以上)"""
        response = api_client.post(
            reverse("users"), data={"username": "longerusername"}
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "error" in response.data

    def test_post_validation_error_emptyusernme(self, api_client):
        """POST: バリデーションエラー(username空文字列)"""
        response = api_client.post(reverse("users"), data={"username": ""})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "error" in response.data

    def test_post_user_already_exists(self, api_client, create_user):
        """POST: 既に存在するユーザーの登録(エラー)"""
        response = api_client.post(reverse("users"), data={"username": "testuser"})
        assert response.status_code == status.HTTP_409_CONFLICT
        assert "error" in response.data

    def test_post_create_user_success(self, api_client):
        """POST: ユーザーを正常に作成(成功)"""
        response = api_client.post(reverse("users"), data={"username": "newuser"})
        assert response.status_code == status.HTTP_201_CREATED
        assert "userId" in response.data
        assert response.data["username"] == "newuser"


@pytest.mark.django_db
class TestUserViewGet:
    def test_get_validation_error(self, api_client):
        """GET: クエリパラメータなし（バリデーションエラー）"""
        response = api_client.get(reverse("users"))
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "error" in response.data

    def test_get_username_and_userid_specified(self, api_client, create_user):
        """GET: username と userid の両方を指定した場合（バリデーションエラー）"""
        response = api_client.get(
            reverse("users"), {"username": "testuser", "userid": create_user.user_id}
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "error" in response.data

    def test_get_user_by_username_success(self, api_client, create_user):
        """GET: username でユーザーを検索（成功）"""
        response = api_client.get(reverse("users"), {"username": "testuser"})
        assert response.status_code == status.HTTP_200_OK
        assert response.data["username"] == "testuser"

    def test_get_user_by_userid_success(self, api_client, create_user):
        """GET: userid でユーザーを検索（成功）"""
        response = api_client.get(reverse("users"), {"userid": create_user.user_id})
        assert response.status_code == status.HTTP_200_OK
        assert response.data["username"] == "testuser"

    def test_get_user_not_found_by_username(self, api_client):
        """GET: 存在しないユーザーを username で検索(エラー)"""
        response = api_client.get(reverse("users"), {"username": "unknown"})
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["error"] == "User not found."

    def test_get_user_not_found_by_userid(self, api_client):
        """GET: 存在しないユーザーを userid で検索(エラー)"""
        response = api_client.get(reverse("users"), {"userid": 99999})
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["error"] == "User not found."

    def test_get_user_with_long_username(self, api_client):
        """GET: 10文字以上の username で検索 (エラー)"""
        response = api_client.get(reverse("users"), {"username": "longusername"})
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "error" in response.data

    def test_get_user_with_empty_username(self, api_client):
        """GET: 空文字のusername で検索 (シリアライザの仕様によりバリデーションエラー)"""
        response = api_client.get(reverse("users"), {"username": " "})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "error" in response.data
