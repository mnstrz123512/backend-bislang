from django.contrib import admin

from games.admins.progress.admin import UserProgressStackedInlineAdmin


class GameAdmin(admin.ModelAdmin):
    list_display = ["type", "answer"]
    inlines = [UserProgressStackedInlineAdmin]
