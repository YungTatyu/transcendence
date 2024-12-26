from django.db import models
from accounts.models import CustomUser


class Friends(models.Model):

    class Meta:
        verbose_name = '友達リスト'
        verbose_name_plural = '友達リスト'

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name = "user_friends")
    friend = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="友達", related_name = "friend_friends")

    def __str__(self):
        return f"{self.friend}"