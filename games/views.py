from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated

from games.models import Type, Game
from account.models import UserProgress
from django.contrib.contenttypes.models import ContentType
from games.serializers import TypeSerializer, GameSerializer, UserProgressSerializer
from rest_framework.response import Response
from account.models import UserAchievement
from rest_framework.decorators import action


class TypeViewset(viewsets.ReadOnlyModelViewSet):
    permission_class = [IsAuthenticated]
    queryset = Type.objects.filter(is_archived=False)
    serializer_class = TypeSerializer


class GameViewset(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Game.objects.filter(is_archived=False)
    serializer_class = GameSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        type = self.request.query_params.get("type")
        if type:
            queryset = queryset.filter(type=type)
        return queryset

    @action(detail=True, methods=["post"], url_path="progress")
    def progress(self, request, pk=None):
        user = request.user
        is_completed = request.data.get("is_completed")
        if not user:
            return Response(
                {"error": "User must be authenticated."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            game = self.get_object()
        except Game.DoesNotExist:
            return Response(
                {"error": "Game not found."}, status=status.HTTP_404_NOT_FOUND
            )

        game_content_type = ContentType.objects.get_for_model(Game)

        progress, created = UserProgress.objects.get_or_create(
            user=user,
            content_type=game_content_type,
            object_id=game.id,
            defaults={"is_completed": is_completed},
        )

        if not created:
            progress.is_completed = is_completed
            progress.save()

        serializer = UserProgressSerializer(progress, context={"request": request})
        if self.check_all_games_completed(user, game.type):
            self.award_achievement(user, game.type)

        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response(serializer.data, status=status_code)

    def check_all_games_completed(self, user, game_type):
        total_games = game_type.games.count()
        completed_games = UserProgress.objects.filter(
            user=user,
            content_type=ContentType.objects.get_for_model(Game),
            object_id__in=game_type.games.values_list("id", flat=True),
            is_completed=True,
        ).count()
        return total_games == completed_games

    def award_achievement(self, user, game_type):
        if game_type.achievement:
            UserAchievement.objects.get_or_create(
                user=user, achievement=game_type.achievement
            )
