"""Tests for the authentication backends of the drf_auth app."""
from django.test import TestCase

from mixer.backend.django import mixer

from .. import auth_backends


class DRFAuthAuthenticationBackendTestCase(TestCase):
    longMessage = True

    def test_backend(self):
        user = mixer.blend('auth.User')
        user.set_password('test')
        user.save()
        b = auth_backends.DRFAuthAuthenticationBackend()
        result = b.authenticate(email=user.email, password='test')
        self.assertEqual(result, user, msg=(
            'Should return the user if credentials match an existing user'))

        result = b.authenticate(email='foo@example.com', password='test')
        self.assertEqual(result, None, msg=(
            'Should return `None` if email does not exist'))

        result = b.authenticate(email=user.email, password='wrong')
        self.assertEqual(result, None, msg=(
            'Should return `None` if password is wrong'))
