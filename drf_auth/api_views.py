import json

from django.conf import settings
from django.contrib.auth import authenticate, login, logout

import requests
from rest_framework import permissions, views, response, status

from . import serializers


FACEBOOK_API_BASE_URL = 'https://graph.facebook.com'


class FacebookLoginAPIView(views.APIView):
    permission_classes = [permissions.AllowAny, ]

    def post(self, request, *args, **kwargs):
        # First, we need to get a token so that we can make more API requests
        resp = requests.get(
            '{}/oauth/access_token?client_id={}&client_secret={}'
            '&grant_type=client_credentials'.format(
                FACEBOOK_API_BASE_URL,
                settings.FACEBOOK_APP_ID,
                settings.FACEBOOK_APP_SECRET))
        # TODO: Handle cases where the response is not OK

        # Next, we check if the given token is valid
        app_access_token = resp.content
        user_access_token = request.data['authResponse']['accessToken']
        resp = requests.get(
            '{}/debug_token?input_token={}&{}'.format(
                FACEBOOK_API_BASE_URL,
                user_access_token,
                app_access_token))
        # TODO: Handle cases where the response is not OK

        # Finally, we request the user-data for that valid token's user-id.
        facebook_user_id = json.loads(resp.content)['data']['user_id']
        resp = requests.get(
            '{}/{}?{}&fields=email,first_name,last_name'.format(
                FACEBOOK_API_BASE_URL,
                facebook_user_id,
                app_access_token))

        # TODO: Create user, if doesn't exist and sign them in, handle special
        # error cases for users that are already connected to FB etc
        return response.Response('OK')


class LoginAPIView(views.APIView):
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
    def post(self, request, *args, **kwargs):
        logout(request._request)
        return response.Response('OK')
