"""Tests for the serializers of the drf_auth app."""
from django.test import TestCase

from mixer.backend.django import mixer

from .. import serializers


class LoginSerializerTestCase(TestCase):
    longMessage = True

    def test_serializer(self):
        user = mixer.blend('auth.User')
        user.set_password('test')

        data = {}
        s = serializers.LoginSerializer(data=data)
        self.assertFalse(s.is_valid(), msg=(
            'Should be invalid if no data is given'))

        data = {'email': 'wrong@example.com', 'password': 'test'}
        s = serializers.LoginSerializer(data=data)
        self.assertFalse(s.is_valid(), msg=(
            'Should be invalid if email does not exist'))

        data = {'email': user.email, 'password': 'something'}
        s = serializers.LoginSerializer(data=data)
        self.assertTrue(s.is_valid(), msg=(
            'Should be valid if all data is given and email does exist.'
            ' Note: Serializer does not check if password is correct. It'
            ' merely checks if the given data makes sense.'))


class FinishSignupSerializerTestCase(TestCase):
    longMessage = True

    def test_serializer(self):
        user = mixer.blend('auth.User')

        data = {}
        s = serializers.FinishSignupSerializer(data=data)
        self.assertFalse(s.is_valid(), msg=(
            'Should be invalid if no data is given'))

        data = {'email': user.email}
        s = serializers.FinishSignupSerializer(data=data)
        self.assertFalse(s.is_valid(), msg=(
            'Should be invalid if the email already exists'))

        data = {'email': 'test@example.com'}
        s = serializers.FinishSignupSerializer(data=data)
        self.assertTrue(s.is_valid(), msg=(
            'Should be valid if new unique email is given')) 
