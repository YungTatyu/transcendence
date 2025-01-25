from django.db import models
from django.utils.timezone import now


class Matches(models.Model):
    match_id = models.AutoField(primary_key=True)
    winner_user_id = models.IntegerField(null=True, blank=True)

    MODE_CHOICES = [("QuickPlay", "QuickPlay"), ("Tournament", "Tournament")]
    mode = models.CharField(choices=MODE_CHOICES, max_length=20)

    start_date = models.DateField(default=now)
    finish_date = models.DateField(null=True, blank=True)
    tournament_id = models.IntegerField(null=True, blank=True)
    parent_match_id = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True
    )
    round = models.PositiveIntegerField(null=True, blank=True)


class MatchParticipants(models.Model):
    match_id = models.ForeignKey(Matches, on_delete=models.CASCADE)
    user_id = models.IntegerField()
    score = models.IntegerField(null=True, blank=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["match_id", "user_id"])]
