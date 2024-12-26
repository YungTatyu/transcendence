from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

# AbstractUserとUserManagerを継承して
# "メールアドレス+パスワード"でログオンするCustomUserクラスを定義

class CustomUser(AbstractUser, UserManager):
    email = models.EmailField(verbose_name="メールアドレス", unique=True, blank=False, null=False)
    thumbnail = models.ImageField(upload_to="images/thumbnail", verbose_name="サムネイル", blank=True, null=True)
    USERNAME_FIELD = 'email' #ログオンIDをユーザー名emailに変更
    REQUIRED_FIELDS = ['username'] #ユーザーを指定するために必要なきー

    def __str__(self):
        return self.email