"""Tests for the middleware classes of the drf_auth app."""
from django.test import RequestFactory, TestCase
from django.core.urlresolvers import reverse

from mixer.backend.django import mixer

from .. import middleware


class FinishSignupMiddlewareTestCase(TestCase):
    def test_middleware(self):
        m = middleware.FinishSignupMiddleware()
        user = mixer.blend('auth.User', email='')

        req = RequestFactory().get('/')
        result = m.process_request(req)
        self.assertEqual(result, None, msg=(
            'Should do nothing if the user is not authenticated.'))

        req.user = user
        result = m.process_request(req)
        expected = reverse('drf_auth_finish_signup')
        self.assertEqual(result.url, expected, msg=(
            'Should redirect if user does not have an email'))

        user.email = 'test@example.com'
        user.save()
        req.user = user
        result = m.process_request(req)
        self.assertEqual(result, None, msg=(
            'Should do nothing if user has an email'))
