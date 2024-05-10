from django.urls import path, include
from rest_framework.routers import DefaultRouter
from games.views import GameTypeViewset

router = DefaultRouter()

router.register(r"type", GameTypeViewset, basename="type")

urlpatterns = [
    path("", include(router.urls)),
]
