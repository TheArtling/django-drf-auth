"""Tests for the API views of the drf_auth app."""
import json

from django.contrib.auth.models import AnonymousUser
from django.test import TestCase

from mixer.backend.django import mixer
from mock import MagicMock, patch
from rest_framework.test import APIRequestFactory, force_authenticate

from .. import api_views
from .. import exceptions
from .. import models


class FacebookLoginAPIViewTestCase(TestCase):
    longMessage = True

    def test_cancel_facebook_login(self):
        req = APIRequestFactory().post('/', data={})
        resp = api_views.FacebookLoginAPIView().as_view()(req, version='v1')
        self.assertEqual(resp.status_code, 400, msg=(
            'Should return 400 if no data is given (i.e. login was'
            ' cancelled).'))

    @patch('drf_auth.api_views.get_app_access_token')
    def test_bad_settings(self, get_app_access_token_mock):
        """
        Should raise exception when we cannot get an app access token.

        This is our fault (bad settings), so we don't show an error to the
        user, we raise an exception and get a notification email and fix the
        settings on the server.

        """
        mock_resp = MagicMock()
        mock_resp.status_code = 400
        get_app_access_token_mock.return_value = mock_resp
        req = APIRequestFactory().post('/', data={'fake': 'data'})
        self.assertRaises(
            exceptions.AccessTokenException,
            api_views.FacebookLoginAPIView().as_view(),
            req, version='v1'
        )

    @patch('drf_auth.api_views.get_app_access_token')
    def test_facebook_api_down(self, get_app_access_token_mock):
        mock_resp = MagicMock()
        mock_resp.status_code = 500
        get_app_access_token_mock.return_value = mock_resp
        req = APIRequestFactory().post('/', data={'fake': 'data'})
        resp = api_views.FacebookLoginAPIView().as_view()(req, version='v1')
        self.assertEqual(resp.status_code, 400, msg=(
            'If Facebook returned not 200 and not 400, something is wrong'
            ' with their API and we should return 400 and show an error'
            ' message to the user (i.e. `Please try again later`).'))

    @patch('drf_auth.api_views.get_debug_token')
    @patch('drf_auth.api_views.get_app_access_token')
    def test_debug_token_not_valid(self, get_app_access_token_mock,
                                   get_debug_token_mock):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        get_app_access_token_mock.return_value = mock_resp
        mock_resp2 = MagicMock()
        mock_resp2.status_code = 400
        get_debug_token_mock.return_value = mock_resp2
        data = {'authResponse': {'accessToken': '123'}}
        req = APIRequestFactory().post('/', data=data, format='json')
        resp = api_views.FacebookLoginAPIView().as_view()(req, version='v1')
        self.assertEqual(resp.status_code, 400, msg=(
            'If Facebook returned anything other than 200, something is either'
            ' wrong with their API or the user has submitted a wrong access'
            ' (probably an attacker). We should return 400 and show an error'
            ' message to the user (i.e. `Please try again again or contact'
            ' us`).'))

    @patch('drf_auth.api_views.get_user_data')
    @patch('drf_auth.api_views.get_debug_token')
    @patch('drf_auth.api_views.get_app_access_token')
    def test_user_data_not_acessible(self, get_app_access_token_mock,
                                     get_debug_token_mock, get_user_data_mock):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        get_app_access_token_mock.return_value = mock_resp
        mock_resp2 = MagicMock()
        mock_resp2.status_code = 200
        mock_resp2.content = json.dumps({'data': {'user_id': '123'}})
        get_debug_token_mock.return_value = mock_resp2
        mock_resp3 = MagicMock()
        mock_resp3.status_code = 400
        data = {'authResponse': {'accessToken': '123'}}
        req = APIRequestFactory().post('/', data=data, format='json')
        resp = api_views.FacebookLoginAPIView().as_view()(req, version='v1')
        self.assertEqual(resp.status_code, 400, msg=(
            'If Facebook returned anything other than 200, something is'
            ' wrong with their API. We should return 400 and show an error'
            ' message to the user (i.e. `Please try again again or contact'
            ' us`).'))

    def _create_mocks(self, get_app_access_token_mock, get_debug_token_mock,
                      get_user_data_mock, facebook_email):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        get_app_access_token_mock.return_value = mock_resp
        mock_resp2 = MagicMock()
        mock_resp2.status_code = 200
        mock_resp2.content = json.dumps({'data': {'user_id': '123'}})
        get_debug_token_mock.return_value = mock_resp2
        mock_resp3 = MagicMock()
        mock_resp3.status_code = 200
        if facebook_email is None:
            mock_resp3.content = json.dumps({})
        else:
            mock_resp3.content = json.dumps({'email': facebook_email})
        get_user_data_mock.return_value = mock_resp3

    @patch('drf_auth.api_views.get_user_data')
    @patch('drf_auth.api_views.get_debug_token')
    @patch('drf_auth.api_views.get_app_access_token')
    def test_django_user_with_fb_email_already_exists(
            self, get_app_access_token_mock, get_debug_token_mock,
            get_user_data_mock):
        user = mixer.blend('auth.User', email='fb@example.com')
        self._create_mocks(
            get_app_access_token_mock, get_debug_token_mock,
            get_user_data_mock, user.email)
        data = {'authResponse': {'accessToken': '123'}}
        req = APIRequestFactory().post('/', data=data, format='json')
        resp = api_views.FacebookLoginAPIView().as_view()(req, version='v1')
        self.assertEqual(resp.status_code, 400, msg=(
            'If we already have a user with email `fb@example.com` and'
            ' Facebook returns that same email to us, then we shall show an'
            ' error message and ask the user to login to his existing account'
            ' and connect to Facebook from there.'))
        self.assertTrue(
            'You have already created an account' in resp.data[
                'non_field_errors'][0])

    @patch('drf_auth.api_views.get_user_data')
    @patch('drf_auth.api_views.get_debug_token')
    @patch('drf_auth.api_views.get_app_access_token')
    def test_case1_disconnect_user(
            self, get_app_access_token_mock, get_debug_token_mock,
            get_user_data_mock):
        user = mixer.blend('auth.User', email='user@example.com')
        mixer.blend('drf_auth.Facebook', user=user, facebook_user_id='123')
        self._create_mocks(
            get_app_access_token_mock, get_debug_token_mock,
            get_user_data_mock, 'user@example.com')
        data = {'authResponse': {'accessToken': '123'}}
        req = APIRequestFactory().post('/', data=data, format='json')
        force_authenticate(req, user)
        resp = api_views.FacebookLoginAPIView().as_view()(req, version='v1')
        self.assertEqual(resp.status_code, 200, msg=(
            'If the user is logged in and triggers the Facebook connect and'
            ' they are already connected, then we delete the Facebook'
            ' connection'))
        self.assertEqual(resp.data, 'Facebook connection deleted')
        fb_user = models.Facebook.objects.all()
        self.assertEqual(fb_user.count(), 0)

    @patch('drf_auth.api_views.get_user_data')
    @patch('drf_auth.api_views.get_debug_token')
    @patch('drf_auth.api_views.get_app_access_token')
    def test_case2_authed_user_already_connected_with_other_account(
            self, get_app_access_token_mock, get_debug_token_mock,
            get_user_data_mock):
        user = mixer.blend('auth.User', email='user@example.com')
        user2 = mixer.blend('auth.User', email='user2@example.com')
        mixer.blend('drf_auth.Facebook', user=user2, facebook_user_id='123')
        self._create_mocks(
            get_app_access_token_mock, get_debug_token_mock,
            get_user_data_mock, 'user@example.com')
        data = {'authResponse': {'accessToken': '123'}}
        req = APIRequestFactory().post('/', data=data, format='json')
        force_authenticate(req, user)
        resp = api_views.FacebookLoginAPIView().as_view()(req, version='v1')
        self.assertEqual(resp.status_code, 400, msg=(
            'If the user is logged in and triggers the Facebook connect and'
            ' they are already connected with another Django account, then we'
            ' show an error and ask to disconnect the other account, first.'))
        self.assertTrue(
            'You have already connected' in resp.data['non_field_errors'][0])

    @patch('drf_auth.api_views.get_user_data')
    @patch('drf_auth.api_views.get_debug_token')
    @patch('drf_auth.api_views.get_app_access_token')
    def test_case3_login_existing_facebook_user(
            self, get_app_access_token_mock, get_debug_token_mock,
            get_user_data_mock):
        user = mixer.blend('auth.User', email='user@example.com')
        mixer.blend('drf_auth.Facebook', user=user, facebook_user_id='123')
        self._create_mocks(
            get_app_access_token_mock, get_debug_token_mock,
            get_user_data_mock, 'user@example.com')
        data = {'authResponse': {'accessToken': '123'}}
        req = APIRequestFactory().post('/', data=data, format='json')
        req.user = AnonymousUser()
        req.session = self.client.session
        resp = api_views.FacebookLoginAPIView().as_view()(req, version='v1')
        self.assertEqual(resp.status_code, 200, msg=(
            'If the user logs in with Facebook and has done it before, they'
            ' should be logged in'))

    @patch('drf_auth.api_views.get_user_data')
    @patch('drf_auth.api_views.get_debug_token')
    @patch('drf_auth.api_views.get_app_access_token')
    def test_case4_new_facebook_user_but_email_already_exists(
            self, get_app_access_token_mock, get_debug_token_mock,
            get_user_data_mock):
        mixer.blend('auth.User', email='fb@example.com')
        self._create_mocks(
            get_app_access_token_mock, get_debug_token_mock,
            get_user_data_mock, 'fb@example.com')
        data = {'authResponse': {'accessToken': '123'}}
        req = APIRequestFactory().post('/', data=data, format='json')
        req.user = AnonymousUser()
        req.session = self.client.session
        resp = api_views.FacebookLoginAPIView().as_view()(req, version='v1')
        self.assertEqual(resp.status_code, 400, msg=(
            'If the user tries to login via Facebook but has already logged'
            ' in via email before (with the same email they use at Facebook),'
            ' we need to show an error and ask the user to login via email'
            ' and then connect to Facebook.'
        ))

    @patch('drf_auth.api_views.get_user_data')
    @patch('drf_auth.api_views.get_debug_token')
    @patch('drf_auth.api_views.get_app_access_token')
    def test_case5_new_user_with_facebook_email(
            self, get_app_access_token_mock, get_debug_token_mock,
            get_user_data_mock):
        self._create_mocks(
            get_app_access_token_mock, get_debug_token_mock,
            get_user_data_mock, 'fb@example.com')
        data = {'authResponse': {'accessToken': '123'}}
        req = APIRequestFactory().post('/', data=data, format='json')
        req.user = AnonymousUser()
        req.session = self.client.session
        resp = api_views.FacebookLoginAPIView().as_view()(req, version='v1')
        self.assertEqual(resp.status_code, 200, msg=(
            'Should create new Django & Facebook instance.'))
        fb_user = models.Facebook.objects.all()
        self.assertEqual(fb_user.count(), 1)

    @patch('drf_auth.api_views.get_user_data')
    @patch('drf_auth.api_views.get_debug_token')
    @patch('drf_auth.api_views.get_app_access_token')
    def test_case6_new_user_without_facebook_email(
            self, get_app_access_token_mock, get_debug_token_mock,
            get_user_data_mock):
        self._create_mocks(
            get_app_access_token_mock, get_debug_token_mock,
            get_user_data_mock, None)
        data = {'authResponse': {'accessToken': '123'}}
        req = APIRequestFactory().post('/', data=data, format='json')
        req.user = AnonymousUser()
        req.session = self.client.session
        resp = api_views.FacebookLoginAPIView().as_view()(req, version='v1')
        self.assertEqual(resp.status_code, 200, msg=(
            'Should create new Django & Facebook instance.'))
        fb_user = models.Facebook.objects.all()
        self.assertEqual(fb_user.count(), 1)

    @patch('drf_auth.api_views.get_user_data')
    @patch('drf_auth.api_views.get_debug_token')
    @patch('drf_auth.api_views.get_app_access_token')
    def test_case7_authed_user_connects_to_facebook(
            self, get_app_access_token_mock, get_debug_token_mock,
            get_user_data_mock):
        user = mixer.blend('auth.User')
        self._create_mocks(
            get_app_access_token_mock, get_debug_token_mock,
            get_user_data_mock, 'fb@example.com')
        data = {'authResponse': {'accessToken': '123'}}
        req = APIRequestFactory().post('/', data=data, format='json')
        force_authenticate(req, user)
        req.session = self.client.session
        resp = api_views.FacebookLoginAPIView().as_view()(req, version='v1')
        self.assertEqual(resp.status_code, 200, msg=(
            'Should create new Facebook instance connected to this user.'))
        fb_user = models.Facebook.objects.all()
        self.assertEqual(fb_user.count(), 1)
        self.assertEqual(fb_user[0].user, user)

    @patch('drf_auth.api_views.get_user_data')
    @patch('drf_auth.api_views.get_debug_token')
    @patch('drf_auth.api_views.get_app_access_token')
    def test_account_disabled(
            self, get_app_access_token_mock, get_debug_token_mock,
            get_user_data_mock):
        user = mixer.blend(
            'auth.User', email='fb@example.com', is_active=False)
        mixer.blend('drf_auth.Facebook', user=user, facebook_user_id='123')
        self._create_mocks(
            get_app_access_token_mock, get_debug_token_mock,
            get_user_data_mock, user.email)
        data = {'authResponse': {'accessToken': '123'}}
        req = APIRequestFactory().post('/', data=data, format='json')
        req.user = AnonymousUser()
        req.session = self.client.session
        resp = api_views.FacebookLoginAPIView().as_view()(req, version='v1')
        self.assertEqual(resp.status_code, 400, msg=(
            'Should show error about acount not being active.'))
        self.assertTrue(
            'Account is disabled' in resp.data['non_field_errors'][0])


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


class FinishSignupAPIViewTestCase(TestCase):
    longMessage = True

    def test_view(self):
        user = mixer.blend('auth.User', email='')
        data = {}
        req = APIRequestFactory().post('/', data=data)
        force_authenticate(req, user)
        resp = api_views.FinishSignupAPIView().as_view()(req, version='v1')
        self.assertEqual(resp.status_code, 400, msg=(
            'Should return 400 if no data is given'))

        data = {'email': 'test@example.com'}
        req = APIRequestFactory().post('/', data=data)
        force_authenticate(req, user)
        resp = api_views.FinishSignupAPIView().as_view()(req, version='v1')
        self.assertEqual(resp.status_code, 200, msg=(
            'Should return 200 if new email could be saved'))
        user.refresh_from_db()
        self.assertEqual(user.email, 'test@example.com')
