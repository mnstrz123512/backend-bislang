from rest_framework import viewsets
from games.models import GameType, Game
from games.serializers import GameTypeSerializer, GameSerializer


class GameTypeViewset(viewsets.ReadOnlyModelViewSet):
    queryset = GameType.objects.all()
    serializer_class = GameTypeSerializer


class GameViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
