from django.db import models

# Create your models here.

class Memo(models.Model):
    title = models.CharField(max_length=150)
    text = models.TextField(blank=True)
    created_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
