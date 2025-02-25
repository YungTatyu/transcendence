from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.timezone import now




class User(models.Model):
    DEFAULT_AVATAR_PATH = "images/default/1.png"

    user_id = models.AutoField(primary_key=True)
    username = models.CharField(validators=[MinLengthValidator(1)], max_length=10)
    # avatar_path = models.CharField(max_length=100, default=DEFAULT_AVATAR_PATH)
    avatar_path = models.ImageField(upload_to="images/uploads/")
    created_at = models.DateField(default=now)

    def __str__(self):
        return self.username
