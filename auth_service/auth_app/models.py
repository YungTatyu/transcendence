from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    """
    Custom manager for the CustomUser model.
    """

    def create_user(self, user_id, mail_address, password=None, **extra_fields):
        """
        Create and return a regular user.
        """
        if not user_id:
            raise ValueError("The user_id field must be set.")
        if not mail_address:
            raise ValueError("The mail_address field must be set.")

        mail_address = self.normalize_email(mail_address)
        user = self.model(user_id=user_id, mail_address=mail_address, **extra_fields)
        user.set_password(password)  # Djangoの `password` フィールドを使う
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    """
    Custom user model with user_id as the primary key.
    """

    user_id = models.CharField(
        max_length=36, primary_key=True, unique=True
    )  # 自動付与しない主キー
    mail_address = models.EmailField(
        unique=True,
        max_length=255,
        verbose_name="Email Address"
    )
    secret_key = models.CharField(
        max_length=128,
        blank=True,
        null=True,
        verbose_name="Secret Key"
    )
    date_joined = models.DateTimeField(auto_now_add=True)

    # Manager
    objects = CustomUserManager()

    # For authentication
    USERNAME_FIELD = "mail_address"
    REQUIRED_FIELDS = ["user_id"]

    def __str__(self):
        return self.mail_address
