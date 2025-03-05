from django.db import models
from django.utils.timezone import now


# Create your models here.
class Friend(models.Model):
    STATUS_PENDING = "pending"
    STATUS_APPROVED = "approved"

    from_user_id = models.IntegerField()
    to_user_id = models.IntegerField()
    MODEL_CHOICES = [(STATUS_PENDING, "pending"), (STATUS_APPROVED, "approved")]
    status = models.CharField(choices=MODEL_CHOICES, max_length=20)
    request_sent_at = models.DateTimeField(default=now)
    approved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["from_user_id", "to_user_id"], name="unique_friend_request"
            )
        ]
