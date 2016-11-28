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
            raise serializers.ValidationError('Email or password incorrect.')
        return data


class FinishSignupSerializer(serializers.Serializer):
    """Serializer to collect the user's email."""
    email = serializers.EmailField()

    class Meta:
        fields = ('email')

    def validate_email(self, data):
        User = get_user_model()
        try:
            User.objects.get(email=data)
            raise serializers.ValidationError(
                'A user with this email already exists.')
        except User.DoesNotExist:
            pass
        return data
