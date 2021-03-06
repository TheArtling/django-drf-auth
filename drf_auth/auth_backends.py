"""Custom authentication backend for the drf_auth app."""
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class EmailAuthenticationBackend(ModelBackend):
    def authenticate(self, **credentials):
        email = credentials.get('email', credentials.get('username'))
        User = get_user_model()
        if email:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return None
            if user.check_password(credentials["password"]):
                return user
        return None


class FacebookAuthenticationBackend(ModelBackend):
    def authenticate(self, **credentials):
        facebook_user = credentials.get('facebook_user')
        if facebook_user:
            return facebook_user.user
        return None
