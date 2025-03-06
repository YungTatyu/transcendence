import os

from django.core.files.storage import default_storage
from django.core.validators import MinLengthValidator
from rest_framework import serializers

from .models import User


class CreateUserSerializer(serializers.Serializer):
    username = serializers.CharField(validators=[MinLengthValidator(1)], max_length=10)


class UserDataSerializer(serializers.Serializer):
    userId = serializers.IntegerField(source="user_id")  # noqa: N815
    username = serializers.CharField(validators=[MinLengthValidator(1)], max_length=10)
    avatarPath = serializers.ImageField(source="avatar_path")  # noqa: N815


class QueryParamSerializer(serializers.Serializer):
    userId = serializers.IntegerField(required=False, source="user_id")  # noqa: N815
    username = serializers.CharField(required=False)

    def validate(self, data):
        """
        username または userid のどちらか一方のみを許可するバリデーション
        """

        username = data.get("username")
        user_id = data.get("user_id")

        if username is None and user_id is None:
            raise serializers.ValidationError(
                "query parameter 'username' or 'userId' is required."
            )

        if username is not None and user_id is not None:
            raise serializers.ValidationError(
                "query parameter 'username' or 'userId' must not be provided together."
            )

        return data


class UsernameSerializer(serializers.ModelSerializer):
    username = serializers.CharField(validators=[MinLengthValidator(1)], max_length=10)

    class Meta:
        model = User
        fields = ["username"]

    def validate(self, data):
        """
        username 重複チェック
        """
        username = data["username"]
        if (
            User.objects.filter(username=username)
            .exclude(user_id=self.instance.user_id)
            .exists()
        ):
            raise serializers.ValidationError({"username": "Username already exists."})
        return data


class AvatarSerializer(serializers.ModelSerializer):
    MAX_FILE_SIZE = 4 * 1024 * 1024

    class Meta:
        model = User
        fields = ["avatar_path"]

    def validate(self, data):
        """
        バリデーションとファイル名更新
        """

        user_id = self.context.get("user_id")

        if "avatar_path" not in data:
            raise serializers.ValidationError({"avatar_path": "No file uploaded."})

        avatar_file = data["avatar_path"]

        if avatar_file.size > self.MAX_FILE_SIZE:
            raise serializers.ValidationError(
                {"avatar_path": "File size must be less than 4MB."}
            )

        # ファイルの拡張子を取得
        ext = os.path.splitext(avatar_file.name)[1].lower()

        # 新しいファイル名
        new_filename = f"avatar_{user_id}{ext}"
        avatar_file.name = new_filename

        return data

    def update(self, instance, validated_data):
        """
        既存の User インスタンスの avatar_path を更新する
        ModelSerializerでserialixer.save()を使うために必要
        """
        # 同じ名前のファイルがあったら古いファイルを削除
        if instance.avatar_path:
            old_avatar_path = instance.avatar_path.path
            if os.path.exists(old_avatar_path):
                default_storage.delete(old_avatar_path)

        # 新しいファイルを保存
        instance.avatar_path = validated_data["avatar_path"]
        instance.save()

        return instance
