from django.db import models
from django.utils.timezone import now


# Create your models here.
class Friends(models.Model):
    from_user_id = models.IntegerField()
    # JWE から from_user_idは固定値
    to_user_id = models.IntegerField()
    MODEL_CHOICES = [("approved", "approved"), ("pending", "pending")]
    status = models.CharField(choices=MODEL_CHOICES, max_length=20)
    request_sent_at = models.DateTimeField(default=now)
    approved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["from_user_id", "to_user_id"], name="unique_friend_request"
            )
        ]
