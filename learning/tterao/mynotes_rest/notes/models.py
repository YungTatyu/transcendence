from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Note(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
