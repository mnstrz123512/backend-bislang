from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from account.serializers.user import BadgeSerializer, LoginSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from account.models import UserAchievement
from account.serializers.user import UserAchievementSerializer
from rest_framework import viewsets, permissions
from account.models import Badge
from rest_framework.decorators import action


@api_view(["POST"])
def login(request):
    serializer = LoginSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(
        username=serializer.validated_data["username"],
        password=serializer.validated_data["password"],
    )

    if not user:
        return Response(
            {"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
        )

    refresh = RefreshToken.for_user(user)
    return Response(
        {
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "profile_image": user.profile_image.url if user.profile_image else None,
            "refresh_token": str(refresh),
            "access_token": str(refresh.access_token),
        }
    )


@api_view(["GET"])
def get_achievements(request):
    user = request.user
    achievements = UserAchievement.objects.filter(user=user)

    serializer = UserAchievementSerializer(achievements, many=True)

    return Response(serializer.data)


class UserAchievementViewset(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = UserAchievement.objects.all()
    serializer_class = UserAchievementSerializer

    @action(detail=False, methods=["get"], url_path="badges")
    def badges(self, request):
        user = request.user
        user_achievements = UserAchievement.objects.filter(user=user)
        badge_ids = user_achievements.values_list("achievement__badges", flat=True)
        badges = Badge.objects.filter(id__in=badge_ids).distinct()
        serializer = BadgeSerializer(badges, many=True, context={"request": request})
        return Response(serializer.data)
