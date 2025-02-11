import pytest
from rest_framework.exceptions import ValidationError

from user_app.serializers import (
    CreateUserSerializer,
    QueryParamSerializer,
    UserDataSerializer,
)


@pytest.mark.parametrize(
    "data, is_valid",
    [
        ({"username": "testuser"}, True),  # 正常ケース
        ({"username": "longusername123"}, False),  # 10文字超過
        ({}, False),  # username がない
    ],
)
def test_create_user_serializer(data, is_valid):
    """CreateUserSerializerのバリデーションテスト"""
    serializer = CreateUserSerializer(data=data)
    assert serializer.is_valid() == is_valid


def test_user_data_serializer():
    """UserDataSerializerのシリアライゼーションテスト"""
    data = {
        "user_id": 1,
        "username": "testuser",
        "avatar_path": "/path/to/avatar.png",
    }
    serializer = UserDataSerializer(data=data)
    assert serializer.is_valid()
    assert serializer.validated_data == data


@pytest.mark.parametrize(
    "data, is_valid",
    [
        ({"user_id": 1}, True),  # user_idのみ
        ({"username": "testuser"}, True),  # usernameのみ
        ({"user_id": 1, "username": "testuser"}, False),  # 両方指定 (エラー)
        ({}, False),  # どちらも指定なし (エラー)
        ({"user_id": "1"}, False),  # user_id が文字列 (エラー)
    ],
)
def test_query_param_serializer(data, is_valid):
    """QueryParamSerializerのバリデーションテスト"""
    serializer = QueryParamSerializer(data=data)

    if is_valid:
        assert serializer.is_valid()
    else:
        with pytest.raises(ValidationError):
            serializer.is_valid(raise_exception=True)
