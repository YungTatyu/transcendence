from django.test import TestCase

from user_app.models import User
from user_app.serializers import SearchUserSerializer


class SearchUserSerializerTest(TestCase):
    def test_valid_serializer(self):
        """正しいデータがシリアライズされるか"""
        user = User(user_id=1, username="testuser", avatar_path="/uploads/test.png")
        serializer = SearchUserSerializer(user)
        expected_data = {
<<<<<<< HEAD
            "userId": 1,
            "username": "testuser",
            "avatarPath": "/uploads/test.png"
=======
            "user_id": 1,
            "username": "testuser",
            "avatar_path": "/uploads/test.png",
>>>>>>> 867c35f ([fix] user serializer and model)
        }
        self.assertEqual(serializer.data, expected_data)
