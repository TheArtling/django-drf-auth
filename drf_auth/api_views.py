import json
import uuid

from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, login, logout

import requests
from rest_framework import permissions, views, response, status

from . import exceptions
from . import models
from . import serializers


FACEBOOK_API_BASE_URL = 'https://graph.facebook.com'


def get_app_access_token():  # pragma: nocover
    """
    Get's an access token from Facebook.

    Helper function that can be mocked in tests.

    """
    resp = requests.get(
        '{}/oauth/access_token?client_id={}&client_secret={}'
        '&grant_type=client_credentials'.format(
            FACEBOOK_API_BASE_URL,
            settings.FACEBOOK_APP_ID,
            settings.FACEBOOK_APP_SECRET))
    return resp


def get_debug_token(app_access_token, user_access_token):  # pragma: nocover
    """
    Validates an user access token from Facebook.

    Helper function that can be mocked in tests.

    """
    resp = requests.get(
        '{}/debug_token?input_token={}&{}'.format(
            FACEBOOK_API_BASE_URL,
            user_access_token,
            app_access_token))
    return resp


def get_user_data(app_access_token, facebook_user_id):  # pragma: nocover
    """
    Retrieves user profile data from Facebook.

    Helper function that can be mocked in tests.

    """
    resp = requests.get(
        '{}/{}?{}&fields=email,first_name,last_name'.format(
            FACEBOOK_API_BASE_URL,
            facebook_user_id,
            app_access_token))
    return resp


class FacebookLoginAPIView(views.APIView):
    """
    Performs a login or signup via Facebook.



    """
    permission_classes = [permissions.AllowAny, ]

    def get_app_access_token(self):
        """
        Fetches access token from Facebook.

        This is needed so that we can make any further API calls.

        """
        resp = get_app_access_token()
        if resp.status_code == 400:
            raise exceptions.AccessTokenException()
        if resp.status_code != 200:
            resp = response.Response(
                {'non_field_errors': [
                    'Facebook login failed, please try again later.'], },
                status=status.HTTP_400_BAD_REQUEST,
            )
            return (resp, False)
        return (resp, True)

    def get_debug_token(self, app_access_token, user_access_token):
        """
        Verifies a given user access token.

        This makes sure that the token that the client sent to us is still
        valid (they expire) and belongs to our own app.

        """
        resp = get_debug_token(app_access_token, user_access_token)
        if resp.status_code != 200:
            resp = response.Response(
                {'non_field_errors': [
                    'Facebook access token could not be verified. Please'
                    ' try one more time. If the problem persists, please'
                    ' reach out to us.'], },
                status=status.HTTP_400_BAD_REQUEST,
            )
            return (resp, False)
        return (resp, True)

    def get_user_data(self, app_access_token, facebook_user_id):
        """
        Fetches user profile data for the given facebook_user_id.

        This is needed so that we can get the user's email address.

        """
        resp = get_user_data(app_access_token, facebook_user_id)
        if resp.status_code != 200:
            resp = response.Response(
                {'non_field_errors': [
                    'Facebook profile data could not be accessed. Please'
                    ' try one more time. If the problem persists, please'
                    ' reach out to us.'], },
                status=status.HTTP_400_BAD_REQUEST,
            )
            return (resp, False)
        return (resp, True)

    def get_facebook_user(self, request_user, facebook_user_id,
                          facebook_email):
        """
        Performs security checks before we proceed to login the user.

        :param request_user: The current user. Can be AnonymousUser.
        :param facebook_user_id: The Facebook user-id that we got from the
          client and have verified.
        :param facebook_email: The email that we have requested from the
          Facebook API.

        :returns: A 3-Tuple with `(facebook_user, response, success)` where
          `facebook_user` is a `Facebook` instance, `response` is either `None`
          or an error response that should be returned and `success` is a
          boolean. If `success` is `False`, you should return the `response`.
          If `success` is `True`, you can proceed to login the returned
          `facebook_user`. That means: If `success` is `True`, there is always
          something in `facebook_user`. If `success` is `False`, there is
          always something in `response`.

        Note: This view can be used to login/signup an AnonymousUser, but it
        can also be used to connect an authenticated user to Facebook or
        disconnect an authenticated and connected user from Facebook.

        In pseudocode, this function would look like below. You can
        see that each if-else branch results in an action (a `case`) at the
        "leafes" of the nested if-else-hierarchy. In order to avoid such a
        deeply nested code structure, the actual function is not implemented
        in this way, but you will find one test-case for each case.

        NOTE: You will find the case names in the code as comments and also
        in the names of the test-functions. Make sure you keep them all in sync
        when you change this code.

        If we have a Facebook instance for that facebook_user_id:
            If current user is authenticated:
                If current user == facebook.user:
                    # Case1: Delete instance, user wants to disconnect
                Else:
                    # Case2: Ask to disconnect from other account first
            Else:
                # Case3: proceed to login
        Else:
            If current user is authenticated:
                # Case7: Create instance, user wants to connect
            Else:
                If is facebook_email given:
                    If django user with that email exists
                        # Case4: Ask to login and connect
                    Else:
                        # Case5: Create Facebook & Django instance and proceed
                                 to login
                Else:
                    # Case6: Create Facebook & Django instance

        """
        User = get_user_model()
        try:
            facebook_user = models.Facebook.objects.get(
                facebook_user_id=facebook_user_id)
        except models.Facebook.DoesNotExist:
            facebook_user = None
        user_with_facebook_email = None
        if facebook_email:
            try:
                user_with_facebook_email = User.objects.get(
                    email=facebook_email)
            except User.DoesNotExist:
                user_with_facebook_email = None

        # Case 2: Ask to disconnect from other account first
        if (facebook_user and
                request_user.is_authenticated() and
                request_user != facebook_user.user):
            error = (
                'You have already connected your Facebook profile to another'
                ' account. Please login to that account and disconnect your'
                ' Facebook profile there, first.')
            return (
                facebook_user,
                response.Response(
                    {'non_field_errors': [error], },
                    status=status.HTTP_400_BAD_REQUEST,
                ),
                False,
            )

        # Case4: Ask to login and connect
        if (not facebook_user and
                not request_user.is_authenticated() and
                facebook_email and
                user_with_facebook_email):
            error = (
                'You have already created an account via email. Please login'
                ' to your account and connect to Facebook after you have'
                ' logged in.')
            return (
                facebook_user,
                response.Response(
                    {'non_field_errors': [error], },
                    status=status.HTTP_400_BAD_REQUEST,
                ),
                False,
            )

        # Case 3: Proceed to login
        if facebook_user and not request_user.is_authenticated():
            return (facebook_user, None, True)

        # Case 1: Delete instance, user wants to disconnect
        if (facebook_user and
                request_user.is_authenticated() and
                request_user == facebook_user.user):
            facebook_user.delete()
            return (
                facebook_user,
                response.Response('Facebook connection deleted'),
                False,
            )

        # Case7: Create instance, user wants to connect
        if not facebook_user and request_user.is_authenticated():
            facebook_user = models.Facebook.objects.create(
                user=request_user, facebook_user_id=facebook_user_id)
            return (facebook_user, None, True)

        # Case5 & 6: Create Facebook & Django instance and proceed to login
        if not facebook_user and not request_user.is_authenticated():
            create_kwargs = {'username': uuid.uuid4()}
            if facebook_email:
                create_kwargs.update({'email': facebook_email})
            user = User.objects.create(**create_kwargs)
            facebook_user = models.Facebook.objects.create(
                user=user, facebook_user_id=facebook_user_id)
            return (facebook_user, None, True)

    def post(self, request, *args, **kwargs):
        if not request.data:
            return response.Response(
                {'non_field_errors': ['Facebook login was cancelled'], },
                status=status.HTTP_400_BAD_REQUEST,
            )

        resp_app_access_token, success = self.get_app_access_token()
        if not success:
            return resp_app_access_token

        resp_debug_token, success = self.get_debug_token(
            resp_app_access_token.content,
            request.data['authResponse']['accessToken']
        )
        if not success:
            return resp_debug_token

        # Finally, we request the user-data for that valid token's user-id.
        facebook_user_id = json.loads(
            resp_debug_token.content)['data']['user_id']
        resp_user_data, success = self.get_user_data(
            resp_app_access_token.content, facebook_user_id)
        if not success:
            return resp_user_data

        facebook_email = json.loads(resp_user_data.content).get('email')
        facebook_user, resp_facebook_user, success = self.get_facebook_user(
            request.user, facebook_user_id, facebook_email)
        if not success:
            return resp_facebook_user

        user = authenticate(facebook_user=facebook_user)
        if user:
            if user.is_active:
                login(request, user)
                return response.Response('OK')

            return response.Response(
                {'non_field_errors': ['Account is disabled'], },
                status=status.HTTP_400_BAD_REQUEST,
            )

        raise exceptions.FacebookLoginException()  # pragma: nocover


class LoginAPIView(views.APIView):
    """Performs a login for the user with the given credentials."""
    serializer_class = serializers.LoginSerializer
    permission_classes = [permissions.AllowAny, ]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return response.Response(
                serializer.errors, status.HTTP_400_BAD_REQUEST)

        user = authenticate(**serializer.data)

        if user:
            if user.is_active:
                login(request, user)
                return response.Response('OK')

            return response.Response(
                {'non_field_errors': ['Account is disabled'], },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return response.Response(
            {'non_field_errors': ['Email or password incorrect'], },
            status=status.HTTP_400_BAD_REQUEST,
        )


class LogoutAPIView(views.APIView):
    """Performs a logout for the current user."""
    def post(self, request, *args, **kwargs):
        logout(request._request)
        return response.Response('OK')
