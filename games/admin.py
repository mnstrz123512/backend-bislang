from django.contrib import admin

from games.admins.type.admin import TypeAdmin
from games.admins.game.admin import GameAdmin
from games.admins.progress.admin import UserProgressAdmin
from games.models import Type, Game, GameUserProgressProxy


admin.site.register(Type, TypeAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(GameUserProgressProxy, UserProgressAdmin)
