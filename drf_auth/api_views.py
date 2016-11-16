from django.contrib.auth import authenticate, login, logout

from rest_framework import permissions, views, response, status

from . import serializers


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
