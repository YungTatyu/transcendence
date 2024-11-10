from django.db import models


# Create your models here.
class Note(models.Model):
    title = models.CharField(max_length=20)
    content = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
