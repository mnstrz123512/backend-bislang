from rest_framework import serializers
from games.models import Type, Game, UserProgress


class TypeSerializer(serializers.ModelSerializer):
    total_games = serializers.SerializerMethodField()
    completed_games = serializers.SerializerMethodField()

    class Meta:
        model = Type
        fields = ["id", "name", "description", "total_games", "completed_games"]

    def get_total_games(self, obj):
        return obj.game_set.count()

    def get_completed_games(self, obj):
        user = self.context.get("request").user
        if user.is_authenticated:
            return UserProgress.objects.filter(
                game__type=obj, user=user, is_completed=True
            ).count()
        else:
            return 0


class GameSerializer(serializers.ModelSerializer):
    type = TypeSerializer()
    is_completed = serializers.SerializerMethodField(read_only=True)
    user_progress_id = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Game
        fields = ["id", "type", "answer", "image", "is_completed", "user_progress_id"]

    def get_is_completed(self, obj):
        # Get the requesting user
        user = self.context["request"].user

        # Check if the user has progress for this game
        user_progress = UserProgress.objects.filter(user=user, game=obj)

        # Return True if the user has progress for this game and it's marked as completed
        return user_progress.exists() and user_progress.first().is_completed

    def get_user_progress_id(self, obj):
        # Get the requesting user
        user = self.context["request"].user

        # Check if the user has progress for this game
        user_progress = UserProgress.objects.filter(user=user, game=obj)

        # Return the user progress ID if the user has progress for this game
        return user_progress.first().id if user_progress.exists() else None


class UserProgressSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProgress
        fields = ["id", "game", "is_completed"]
