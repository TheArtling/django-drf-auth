"""URLs for the drf_auth app."""
from django.conf.urls import url

from . import api_views


urlpatterns = [
    url(r'^fb-login/$',
        api_views.FacebookLoginAPIView.as_view(),
        name='drf_auth_api_facebook_login'),
    url(r'^login/$',
        api_views.LoginAPIView.as_view(),
        name='drf_auth_api_session_login'),
    url(r'^logout/$',
        api_views.LogoutAPIView.as_view(),
        name='drf_auth_api_session_logout'),
    url(r'^finish-signup/$',
        api_views.FinishSignupAPIView.as_view(),
        name='drf_auth_api_finish_signup'),
]
