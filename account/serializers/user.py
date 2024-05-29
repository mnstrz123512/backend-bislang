from rest_framework import serializers
from account.models import Achievement, CustomUser, UserAchievement, Badge
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username", "first_name", "last_name", "email", "profile_image"]
        read_only_fields = ("email",)  # if email shouldn't be changed


class TokenPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["email"] = user.email
        token["first_name"] = user.first_name
        token["last_name"] = user.last_name
        token["profile_image"] = user.profile_image.url if user.profile_image else None

        return token


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        exclude = ["created_at", "updated_at"]


class AchievementSerializer(serializers.ModelSerializer):
    badges = BadgeSerializer(many=True)

    class Meta:
        model = Achievement
        exclude = ["created_at", "updated_at"]


class UserAchievementSerializer(serializers.ModelSerializer):
    achievement = AchievementSerializer()

    class Meta:
        model = UserAchievement
        exclude = ["created_at", "updated_at"]
