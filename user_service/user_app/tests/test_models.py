from django.test import TestCase

from user_app.models import User


class UserModelTest(TestCase):
    def setUp(self):
        """テスト用のデータをセットアップ"""
        self.user = User.objects.create(
            username="testuser", avatar_path="/uploads/test.png"
        )

    def test_create_user(self):
        """ユーザー作成が正常に動作することを確認"""
        user = User.objects.get(username="testuser")
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.avatar_path, "/uploads/test.png")

    def test_user_string_representation(self):
        """__str__ メソッドが正しく動作するか"""
        self.assertEqual(str(self.user), "testuser")
