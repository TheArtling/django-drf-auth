from django.shortcuts import redirect


class FinishSignupMiddleware(object):
    def process_request(self, request):
        if request.user.is_authenticated():
            if not request.user.email:
                if '/finish-signup/' not in request.path:
                    return redirect('drf_auth_finish_signup')
        return None
