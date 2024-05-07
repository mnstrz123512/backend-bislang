import random
import os
import requests

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.hashers import make_password
from django.core.files.base import ContentFile
from django.contrib.auth import get_user_model

from google.oauth2.id_token import verify_oauth2_token
from google.auth.transport import requests as google_requests

from account.serializers.google import GoogleSignInSerializer


@api_view(["POST"])
def sign_in_with_google(request):
    serializer = GoogleSignInSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    id_token = serializer.validated_data["id_token"]

    User = get_user_model()

    try:
        id_info = verify_oauth2_token(
            id_token, google_requests.Request(), os.getenv("GOOGLE_CLIENT_ID")
        )
    except ValueError as e:
        return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

    # Extract required user information
    email = id_info["email"]
    first_name = id_info.get("given_name", "")
    last_name = id_info.get("family_name", "")
    profile_image_url = id_info.get("picture", None)

    # Check if user exists, if not, create user
    user, created = User.objects.get_or_create(
        username=email,
        defaults={
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "password": make_password(str(random.randint(10000000, 99999999))),
            "profile_image": profile_image_url or "",
        },
    )

    if profile_image_url and created:
        response = requests.get(profile_image_url)
        if response.status_code == 200:
            # Assuming your ImageField is named 'profile_image'
            user.profile_image.save(
                f"{user.username}_profile.jpg", ContentFile(response.content), save=True
            )
            user.save()

    if user.profile_image:
        # Build the full URL for the profile image
        profile_image_full_url = request.build_absolute_uri(user.profile_image.url)
    else:
        profile_image_full_url = None

    # Generate tokens
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)

    user_data = {
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "profile_image": profile_image_full_url,
        "access_token": access_token,
        "refresh_token": refresh_token,
    }

    return Response(user_data)
