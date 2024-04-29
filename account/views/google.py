from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken
import requests
import random
import os
import json

class GoogleView(APIView):
    def post(self, request, *args, **kwargs):
        code = request.GET.get('code')
        
        if not code:
            return Response({"error": "Invalid code"}, status=status.HTTP_400_BAD_REQUEST)

        # Exchange the code for a token
        url = 'https://oauth2.googleapis.com/token'
        data = {
            'code': code,
            'client_id': os.environ.get('GOOGLE_CLIENT_ID'),  
            'client_secret': os.environ['GOOGLE_CLIENT_SECRET'], 
            'redirect_uri': 'http://localhost:8000', 
            'grant_type': 'authorization_code',
        }
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = requests.post(url, data=data, headers=headers)
        response_data = response.json()
        
        print(response_data)

        # Extract the id_token and verify it
        id_token = response_data.get('id_token')
        if id_token:
            verify_url = f'https://oauth2.googleapis.com/tokeninfo?id_token={id_token}'
            verify_response = requests.get(verify_url)
            verify_data = verify_response.json()

            email = verify_data.get('email')
            name = verify_data.get('name')

            # Check if user exists, if not, create user
            user, created = User.objects.get_or_create(
                username=email, defaults={
                    'email': email,
                    'first_name': name.split(' ')[0],
                    'last_name': ' '.join(name.split(' ')[1:]),
                    'password': make_password(str(random.randint(10000000, 99999999)))
                }
            )

            # Generate tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            # Prepare user data and tokens for response
            user_data = {
                'user': {
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email_address': user.email,
                },
                'tokens': {
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                }
            }

            return Response(user_data)

        return Response({'error': 'Failed to authenticate'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
