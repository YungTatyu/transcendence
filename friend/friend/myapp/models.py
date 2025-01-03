from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class FriendRequest(models.Model):
	from_user = models.ForeignKey(User, related_name='sent_request', on_delete=models.CASCADE)
	to_user = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
	status = models.CharField(max_length=10, choices=(('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')), default='pending')