"""Tests for the API views of the drf_auth app."""
from django.test import TestCase

from mixer.backend.django import mixer
from rest_framework.test import APIRequestFactory, force_authenticate

from .. import api_views


class FacebookLoginAPIViewTestCase(TestCase):
    longMessage = True

    def test_view(self):
        pass


class LoginAPIViewTestCase(TestCase):
    longMessage = True

    def test_view(self):
        pass


class LogoutAPIViewTestCase(TestCase):
    longMessage = True

    def test_view(self):
        user = mixer.blend('auth.User')
        req = APIRequestFactory().post('/')
        req.session = self.client.session
        force_authenticate(req, user)
        resp = api_views.LogoutAPIView().as_view()(req, version='v1')
        self.assertEqual(resp.status_code, 200, msg=(
            'Should be callable by anyone'))
