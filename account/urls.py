from django.contrib import admin
from django.urls import include, path
from account.views.google import sign_in_with_google
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from account.views.user import login, get_achievements, UserAchievementViewset
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r"achievements", UserAchievementViewset, basename="achievements")

urlpatterns = [
    path("sign_in_with_google/", sign_in_with_google, name="google"),
    path("login/", login, name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path(r"", include(router.urls)),
]
