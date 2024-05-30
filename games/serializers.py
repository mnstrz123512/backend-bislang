from rest_framework import serializers
from games.models import Type, Game
from account.models import UserProgress
from django.contrib.contenttypes.models import ContentType


class TypeSerializer(serializers.ModelSerializer):
    total_games = serializers.SerializerMethodField()
    total_completed_games = serializers.SerializerMethodField()

    class Meta:
        model = Type
        exclude = ["is_archived"]

    def get_total_games(self, obj):
        # Total games for this type
        return Game.objects.filter(type=obj).count()

    def get_total_completed_games(self, obj):
        user = self.context.get("request").user
        if user.is_authenticated:
            game_content_type = ContentType.objects.get_for_model(Game)
            # Fetch all Game IDs of this type
            game_ids = Game.objects.filter(type=obj).values_list("id", flat=True)

            return UserProgress.objects.filter(
                content_type=game_content_type,
                object_id__in=game_ids,
                user=user,
                is_completed=True,
            ).count()
        else:
            return 0


class GameSerializer(serializers.ModelSerializer):
    type = TypeSerializer()
    is_completed = serializers.SerializerMethodField(read_only=True)
    user_progress_id = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Game
        exclude = ["is_archived"]

    def get_is_completed(self, obj):
        user = self.context["request"].user
        game_content_type = ContentType.objects.get_for_model(Game)

        user_progress = UserProgress.objects.filter(
            user=user, content_type=game_content_type, object_id=obj.id
        )

        return user_progress.exists() and user_progress.first().is_completed

    def get_user_progress_id(self, obj):
        user = self.context["request"].user
        game_content_type = ContentType.objects.get_for_model(Game)

        user_progress = UserProgress.objects.filter(
            user=user, content_type=game_content_type, object_id=obj.id
        )

        return user_progress.first().id if user_progress.exists() else None


class UserProgressSerializer(serializers.ModelSerializer):
    game_details = serializers.SerializerMethodField()

    content_type = serializers.SlugRelatedField(
        queryset=ContentType.objects.filter(model="game"),
        slug_field="model",
        write_only=True,
    )
    object_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = UserProgress
        fields = ["id", "content_type", "object_id", "is_completed", "game_details"]

    def get_game_details(self, obj):
        """Serialize the game details if the related object is a Game"""
        if isinstance(obj.content_object, Game):
            return GameSerializer(obj.content_object, context=self.context).data
        return None
