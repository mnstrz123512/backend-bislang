from django.contrib import admin
from games.models import Game
from .forms import TypeForm


class GameStackedInline(admin.StackedInline):
    model = Game
    extra = 0


class TypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    form = TypeForm
    inlines = [
        GameStackedInline,
    ]
