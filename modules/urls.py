from django.urls import path, include
from rest_framework.routers import DefaultRouter
from modules.views import ModuleViewset

router = DefaultRouter()

router.register(r"", ModuleViewset, basename="modules")

urlpatterns = [
    path("", include(router.urls)),
]
