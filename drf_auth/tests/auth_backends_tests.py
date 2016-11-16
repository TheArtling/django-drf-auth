"""Tests for the authentication backends of the drf_auth app."""
from django.test import TestCase

from mixer.backend.django import mixer

from .. import auth_backends


class EmailAuthenticationBackendTestCase(TestCase):
    longMessage = True

    def test_backend(self):
        user = mixer.blend('auth.User')
        user.set_password('test')
        user.save()
        b = auth_backends.EmailAuthenticationBackend()
        result = b.authenticate(email=user.email, password='test')
        self.assertEqual(result, user, msg=(
            'Should return the user if credentials match an existing user'))

        result = b.authenticate(email='foo@example.com', password='test')
        self.assertEqual(result, None, msg=(
            'Should return `None` if email does not exist'))

        result = b.authenticate(email=user.email, password='wrong')
        self.assertEqual(result, None, msg=(
            'Should return `None` if password is wrong'))


class FacebookAuthenticationBackendTestCase(TestCase):
    longMessage = True

    def test_backend(self):
        facebook_user = mixer.blend('drf_auth.Facebook')
        b = auth_backends.FacebookAuthenticationBackend()
        result = b.authenticate()
        self.assertEqual(result, None, msg=(
            'Should return `None` if no `Facebook` instance is given'))
        result = b.authenticate(facebook_user=facebook_user)
        self.assertEqual(result, facebook_user.user, msg=(
            'Should return the user that is tied to the given `Facebook`'
            ' instance.'))
