from django.test import TestCase
from django.urls import reverse

class HealthCheckTests(TestCase):
    def test_health_check(self):
        """
        GETリクエストを /health/ エンドポイントに送信し、
        ステータスコード200と期待されるJSONレスポンスを確認します。
        """
        url = reverse('health-check')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'status': 'healthy'})
