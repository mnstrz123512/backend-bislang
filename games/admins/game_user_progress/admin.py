from django.contrib import admin

from games.models import UserProgress


class UserProgressAdmin(admin.ModelAdmin):
    list_display = ["game", "user", "is_completed"]
    search_fields = ["game__answer", "user__username"]
    list_filter = ["is_completed"]


class UserProgressStackedInlineAdmin(admin.StackedInline):
    extra = 0
    model = UserProgress
