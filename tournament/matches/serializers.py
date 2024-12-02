from rest_framework import serializers
from .models import Tournament, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'mail_address', 'password', 'created_at']


class TournamentDeserializer(serializers.ModelSerializer):
    players = serializers.ListField(
        child=serializers.CharField(max_length=20),
        min_length=2,
    )
    owner_user = serializers.CharField(max_length=20)

    def validate_players(self, value):
        try:
            player_ids = [str(player) for player in value]
        except ValueError:
            raise serializers.ValidationError("players value error.")
        if len(player_ids) < 2:
            raise serializers.ValidationError("At least two players are required.")
        return player_ids 

    def validate_owner_user(self, value):
        print("owner_user", value)
        if not value:
            raise serializers.ValidationError("Owner user is required.")
        return value

    class Meta:
        model = Tournament
        fields = ['players', 'owner_user']


class TournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = ['owner_user_id', 'status', 'created_at', 'now_round', 'total_round', 'id']
