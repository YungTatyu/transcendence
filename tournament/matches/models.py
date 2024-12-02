from django.db import models

class User(models.Model):
    name = models.CharField(max_length=20, unique=True)
    mail_address = models.EmailField(unique=True)
    password = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)


class Tournament(models.Model):
    owner_user_id = models.IntegerField(default=0)
    status = models.CharField(max_length=20, default="BeforeStarting")
    created_at = models.DateTimeField(auto_now_add=True)
    now_round = models.IntegerField(default=1)
    total_round = models.IntegerField()


class Match(models.Model):
    winner_user_id = models.IntegerField(default=0)
    mode = models.CharField(max_length=20, default="Quick")
    created_at = models.DateTimeField(auto_now_add=True)
    tournament_id = models.IntegerField()
    parent_match_id = models.IntegerField(null=True)
    round = models.IntegerField()

    def __str__(self):
        return f"{self.id} {self.winner_user_id} {self.mode} {self.created_at} {self.tournament_id} {self.parent_match_id} {self.round}"


class MatchParticipant(models.Model):
    match_id = models.IntegerField()
    user_id = models.IntegerField()
    score = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.id} {self.match_id} {self.user_id} {self.score}"
