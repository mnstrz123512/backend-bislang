from django.contrib import admin

from account.models import UserProgress
from games.models import Game
from django.contrib.contenttypes.admin import GenericStackedInline
from django.contrib.contenttypes.models import ContentType


class UserProgressAdmin(admin.ModelAdmin):
    list_display = ["get_game", "user", "is_completed"]
    search_fields = ["user__username"]
    list_filter = ["is_completed"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        game_content_type = ContentType.objects.get_for_model(Game)
        return qs.filter(content_type=game_content_type)

    def get_game(self, obj):
        if isinstance(obj.content_object, Game):
            return obj.content_object
        return "Not a Game"

    get_game.short_description = "Game"

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "content_type":
            kwargs["queryset"] = ContentType.objects.filter(model="game")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class UserProgressStackedInlineAdmin(GenericStackedInline):
    model = UserProgress
    extra = 0
    ct_fk_field = "object_id"
    ct_field = "content_type"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        game_content_type = ContentType.objects.get_for_model(Game)
        return qs.filter(content_type=game_content_type)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "content_type":
            kwargs["queryset"] = ContentType.objects.filter(model="game")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
