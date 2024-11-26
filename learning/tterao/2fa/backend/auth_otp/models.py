from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


# ユーザー作成時の2FA設定
class UserTwoFactorSetup(models.Model):
    username = models.CharField(max_length=150)
    password = models.CharField(max_length=128)
    email = models.EmailField()
    otp_secret = models.CharField(max_length=64)

    REQUIRED_FIELDS = ["username", "password", "email"]


# ログイン時の2FA検証
class UserTwoFactorVerification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp_secret = models.CharField(max_length=64)
