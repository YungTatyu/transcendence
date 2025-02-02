from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=20)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = ('username','email', 'password')
        #passworedをwriteonlyにすることでクライアントは読み込みはできなくなる
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer): 
    username = serializers.CharField(max_length=20)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        #usernameとpasswordを検証
        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError('ログイン失敗: ユーザー名またはパスワードが正しくありません')

        # 認証が成功した場合、ユーザー情報を返す
        data['user'] = user
        return data


class UpdateUsernameSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=20)

    def validate_username(self, value):
        # username の一意性をチェック
        if self.instance.__class__.objects.filter(username=value).exclude(pk=self.instance.pk).exists():
            raise serializers.ValidationError("このユーザー名はすでに使用されています。")
        return value

    def update(self, instance, validated_data):
        # username を更新
        instance.username = validated_data.get('username', instance.username)
        instance.save()
        return instance