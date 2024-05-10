from django.contrib import admin

from games.admins.game_type.admin import GameTypeAdmin
from games.admins.game.admin import GameAdmin
from .models import GameType, Game


admin.site.register(GameType, GameTypeAdmin)
admin.site.register(Game, GameAdmin)
