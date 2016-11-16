"""URLs for the drf_auth app."""
from django.conf.urls import url

from . import api_views


urlpatterns = [
    url(r'^login/$',
        api_views.LoginAPIView.as_view(),
        name='drf_auth_api_login'),
    url(r'^logout/$',
        api_views.LogoutAPIView.as_view(),
        name='drf_auth_api_logout'),
]
