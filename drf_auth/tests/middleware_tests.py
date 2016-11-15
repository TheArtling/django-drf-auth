"""Tests for the middleware classes of the drf_auth app."""
from django.test import TestCase

from .. import middleware


class FinishSignupMiddlewareTestCase(TestCase):
    def test_middleware(self):
        m = middleware.FinishSignupMiddleware()
