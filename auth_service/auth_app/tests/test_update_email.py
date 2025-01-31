from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from auth_app.models import CustomUser
import jwt

class UpdateEmailViewTest(TestCase):
    """
    UpdateEmailView のテスト
    """

    def setUp(self):
        """
        テスト前の初期セットアップ
        """
        self.client = APIClient()

        # テスト用ユーザ作成
        self.user = CustomUser.objects.create_user(
            user_id="test-user-123",
            mail_address="old@example.com",
            password="securepassword",
        )

        # JWT トークンの作成（本来は認証サーバーから取得するが、テストでは直接作成）
        self.token_payload = {"user_id": self.user.user_id}
        self.token = jwt.encode(self.token_payload, "test_secret", algorithm="HS256")

        self.headers = {"HTTP_AUTHORIZATION": f"Bearer {self.token}"}
        self.url = reverse("update_email")

    def test_update_email_success(self):
        """
        正常にメールアドレスを更新できることを確認
        """
        response = self.client.put(
            self.url, 
            {"email": "new@example.com"}, 
            format="json", 
            **self.headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Email updated successfully.")

        # DB の値が更新されているか確認
        self.user.refresh_from_db()
        self.assertEqual(self.user.mail_address, "new@example.com")

    def test_update_email_missing(self):
        """
        email がリクエストボディに存在しない場合 400 エラー
        """
        response = self.client.put(self.url, {}, format="json", **self.headers)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "Email is required.")

    def test_update_email_invalid_format(self):
        """
        不正なフォーマットのメールアドレスを指定した場合 400 エラー
        """
        response = self.client.put(
            self.url, 
            {"email": "invalid-email"}, 
            format="json", 
            **self.headers
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "Invalid email format.")

    def test_update_email_conflict(self):
        """
        既に存在するメールアドレスを指定した場合 409 エラー
        """
        # 競合する別のユーザを作成
        CustomUser.objects.create_user(
            user_id="other-user-456",
            mail_address="existing@example.com",
            password="securepassword",
        )

        response = self.client.put(
            self.url, 
            {"email": "existing@example.com"}, 
            format="json", 
            **self.headers
        )
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.json()["error"], "This email address is already in use.")

    def test_update_email_unauthorized(self):
        """
        Authorization ヘッダーなしでリクエストした場合 401 エラー
        """
        response = self.client.put(self.url, {"email": "new@example.com"}, format="json")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()["error"], "Authorization header missing")

