from rest_framework import serializers


class GoogleSignIn(serializers.Serializer):
    id_token = serializers.CharField()
    
    def validate(self, data):
        