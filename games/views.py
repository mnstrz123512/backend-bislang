from rest_framework import viewsets, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

from games.models import Type, Game, UserProgress
from games.serializers import TypeSerializer, GameSerializer, UserProgressSerializer
from rest_framework.response import Response


class TypeViewset(viewsets.ReadOnlyModelViewSet):
    permission_class = [IsAuthenticated]
    queryset = Type.objects.all()
    serializer_class = TypeSerializer


class GameViewset(viewsets.ReadOnlyModelViewSet):
    permission_class = [IsAuthenticated]
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["type"]


class UserProgressViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserProgress.objects.all()
    serializer_class = UserProgressSerializer
    http_method_names = ["get", "post"]

    def get_queryset(self):
        return UserProgress.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        game_id = request.data.get("game")
        user = request.user

        # Try to get the existing progress object, or create a new one if it doesn't exist
        progress, created = UserProgress.objects.get_or_create(
            user=user, game_id=game_id
        )

        # Update the progress object with data from the request
        serializer = self.get_serializer(progress, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Determine the appropriate status code
        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response(serializer.data, status=status_code)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
