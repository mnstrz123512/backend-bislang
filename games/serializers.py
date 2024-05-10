from rest_framework import serializers
from games.models import GameType, Game


class GameTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameType
        fields = ["id", "name", "description"]


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ["id", "name", "game_type", "answer", "image"]
