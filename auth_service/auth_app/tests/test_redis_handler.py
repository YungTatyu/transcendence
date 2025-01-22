from django.test import TestCase

from auth_app.utils.redis_handler import RedisHandler


class RedisHandlerTestCase(TestCase):
    def setUp(self):
        """テスト用データを設定"""
        self.key = "test_key"
        self.value = "test_value"

    def tearDown(self):
        """テスト後にキャッシュをクリア"""
        RedisHandler.delete(self.key)

    def test_set_and_get(self):
        """Redisに値を設定して取得するテスト"""
        RedisHandler.set(self.key, self.value, timeout=60)
        result = RedisHandler.get(self.key)
        self.assertEqual(result, self.value)

    def test_get_nonexistent_key(self):
        """存在しないキーを取得するテスト"""
        result = RedisHandler.get("nonexistent_key")
        self.assertIsNone(result)

    def test_delete(self):
        """Redisから値を削除するテスト"""
        RedisHandler.set(self.key, self.value, timeout=60)
        RedisHandler.delete(self.key)
        result = RedisHandler.get(self.key)
        self.assertIsNone(result)

    def test_exists(self):
        """Redisにキーが存在するか確認するテスト"""
        RedisHandler.set(self.key, self.value, timeout=60)
        self.assertTrue(RedisHandler.exists(self.key))

        RedisHandler.delete(self.key)
        self.assertFalse(RedisHandler.exists(self.key))
