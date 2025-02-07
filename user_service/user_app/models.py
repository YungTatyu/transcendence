from django.db import models
from django.utils.timezone import now


class User(models.Model):
    DEFAULT_AVATAR_PATH = "/default/1.png"

    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=10)
    avatar_path = models.CharField(max_length=100, default=DEFAULT_AVATAR_PATH)
    created_at = models.DateField(default=now)
