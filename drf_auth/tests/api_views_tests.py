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
        user = mixer.blend('auth.User', is_active=False)
        user.set_password('test')
        user.save()
        data = {}
        req = APIRequestFactory().post('/', data=data)
        resp = api_views.LoginAPIView().as_view()(req, version='v1')
        self.assertEqual(resp.status_code, 400, msg=(
            'Should return 400 if no data is given'))

        data = {'email': user.email, 'password': 'wrong'}
        req = APIRequestFactory().post('/', data=data)
        resp = api_views.LoginAPIView().as_view()(req, version='v1')
        self.assertEqual(resp.status_code, 400, msg=(
            'Should return 400 if wrong password is given'))

        data = {'email': user.email, 'password': 'test'}
        req = APIRequestFactory().post('/', data=data)
        resp = api_views.LoginAPIView().as_view()(req, version='v1')
        self.assertEqual(resp.status_code, 400, msg=(
            'Should return 400 if user is inactive'))

        user.is_active = True
        user.save()
        data = {'email': user.email, 'password': 'test'}
        req = APIRequestFactory().post('/', data=data)
        req.session = self.client.session
        resp = api_views.LoginAPIView().as_view()(req, version='v1')
        self.assertEqual(resp.status_code, 200, msg=(
            'Should return 200 if user has logged in'))


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
