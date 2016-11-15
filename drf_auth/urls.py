"""URLs for the drf_auth app."""
from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^finish-signup/$',
        views.FinishSignupView.as_view(),
        name='drf_auth_finish_signup'),
]
