from django.contrib import admin

from games.admins.game_user_progress.admin import UserProgressStackedInlineAdmin


class GameAdmin(admin.ModelAdmin):
    list_display = ["type", "answer"]
    inlines = [UserProgressStackedInlineAdmin]
