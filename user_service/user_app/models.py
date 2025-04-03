from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.timezone import now

# アップロード画像は /media/images/uploads/ に保存される


class User(models.Model):
    DEFAULT_AVATAR_PATH = "images/default/default_image.png"

    user_id = models.AutoField(primary_key=True)
    username = models.CharField(validators=[MinLengthValidator(1)], max_length=10)
    avatar_path = models.ImageField(
        upload_to="images/uploads/", default=DEFAULT_AVATAR_PATH
    )
    created_at = models.DateField(default=now)

    def __str__(self):
        return self.username
