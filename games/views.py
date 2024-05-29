from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated

from games.models import Type, Game
from account.models import UserProgress
from django.contrib.contenttypes.models import ContentType
from games.serializers import TypeSerializer, GameSerializer, UserProgressSerializer
from rest_framework.response import Response


class TypeViewset(viewsets.ReadOnlyModelViewSet):
    permission_class = [IsAuthenticated]
    queryset = Type.objects.all()
    serializer_class = TypeSerializer


class GameViewset(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def get_queryset(self):
        queryset = Game.objects.all()
        type = self.request.query_params.get("type")
        if type:
            queryset = queryset.filter(type=type)
        return queryset


class GameUserProgressViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProgressSerializer
    http_method_names = ["get", "post"]

    def get_queryset(self):
        user = self.request.user
        game_content_type = ContentType.objects.get_for_model(Game)
        return UserProgress.objects.filter(user=user, content_type=game_content_type)

    def create(self, request, *args, **kwargs):
        user = request.user
        game_id = request.data.get("game")

        if not game_id:
            return Response(
                {"error": "Game ID must be provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            game = Game.objects.get(pk=game_id)
        except Game.DoesNotExist:
            return Response(
                {"error": "Game not found."}, status=status.HTTP_404_NOT_FOUND
            )

        game_content_type = ContentType.objects.get_for_model(Game)

        progress, created = UserProgress.objects.get_or_create(
            user=user, content_type=game_content_type, object_id=game.id
        )

        serializer = self.get_serializer(progress, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response(serializer.data, status=status_code)
