from django.db import models
from django.utils.timezone import now


class Tournaments(models.Model):
    tournament_id = models.AutoField(primary_key=True)
    start_date = models.DateField(default=now)
    finish_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return (
            f"Tournament {self.tournament_id} ({self.start_date} - {self.finish_date})"
        )
