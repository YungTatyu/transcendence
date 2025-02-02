from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    """
    Custom manager for the CustomUser model.
    """

    def create_user(self, user_id, email, secret_key, password=None, **extra_fields):
        """
        Create and return a regular user.
        """
        if not user_id:
            raise ValueError("The user_id field must be set.")
        if not email:
            raise ValueError("The email field must be set.")

        email = self.normalize_email(email)
        user = self.model(
            user_id=user_id, email=email, secret_key=secret_key, **extra_fields
        )
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
    email = models.EmailField(unique=True, max_length=255, verbose_name="Email Address")
    secret_key = models.CharField(
        max_length=128, blank=True, null=True, verbose_name="Secret Key"
    )
    date_joined = models.DateTimeField(auto_now_add=True)

    # Manager
    objects = CustomUserManager()

    # For authentication
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["user_id"]

    def __str__(self):
        return self.email
