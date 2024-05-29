from django.urls import path, include
from rest_framework.routers import DefaultRouter
from games.views import GameViewset, TypeViewset, GameUserProgressViewSet

router = DefaultRouter()

router.register(r"type", TypeViewset, basename="type")
router.register(r"progress", GameUserProgressViewSet, basename="game-progress")
router.register(r"", GameViewset, basename="game")

urlpatterns = [
    path("", include(router.urls)),
]
