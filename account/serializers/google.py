from rest_framework import serializers


class GoogleSignInSerializer(serializers.Serializer):
    id_token = serializers.CharField()
