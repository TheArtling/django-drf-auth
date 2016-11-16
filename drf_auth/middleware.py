from django.core.urlresolvers import reverse
from django.shortcuts import redirect


class FinishSignupMiddleware(object):
    """
    Checks if the current user has an email address.

    If not, we assume that the user has signed up via Facebook and did not
    permit to share the email, so we need to present a form to the user and
    collect the email before we let them into our service.

    """
    def process_request(self, request):
        if not hasattr(request, 'user'):
            return None
        if request.user.is_authenticated():
            if not request.user.email:
                admin_url = reverse('admin:index')
                if request.path.startswith(admin_url):
                    return None
                finish_signup_url = reverse('drf_auth_finish_signup')
                if not request.path == finish_signup_url:
                    return redirect(finish_signup_url)
        return None
