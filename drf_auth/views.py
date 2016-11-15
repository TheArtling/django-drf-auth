"""Views for the drf_auth app."""
from django.views.generic import TemplateView


class FinishSignupView(TemplateView):
    template_name = 'drf_auth/finish_signup.html'
