from django.contrib import admin

from games.admins.type.admin import TypeAdmin
from games.admins.game.admin import GameAdmin
from games.admins.game_user_progress.admin import UserProgressAdmin
from .models import Type, Game, UserProgress


admin.site.register(Type, TypeAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(UserProgress, UserProgressAdmin)
