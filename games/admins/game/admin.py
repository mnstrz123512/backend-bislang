from django.contrib import admin


class GameAdmin(admin.ModelAdmin):
    list_display = ("game_type", "answer")
