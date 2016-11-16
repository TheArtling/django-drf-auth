"""Serializers for the drf_auth app."""
from django.contrib.auth import get_user_model

from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    """Serializer for the login API."""
    email = serializers.EmailField()
    password = serializers.CharField()

    class Meta:
        fields = ('email', 'password')

    def validate(self, data):
        User = get_user_model()
        try:
            User.objects.get(email=data.get('email'))
        except User.DoesNotExist:
            raise serializers.ValidationError("Email or password incorrect.")
        return data
