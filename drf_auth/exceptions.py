"""Exceptions for the drf_auth app."""


class AccessTokenException(Exception):  # pragma: nocover
    """
    Raised when we could not get an app access token from Facebook.

    This can happen when our settings are wrong. Facebook will return a 400
    response, but we don't want to show this to the user, because it is our
    own fault. We will raise this exception instead.

    """
    def __init__(self, message=None):
        if message is None:
            message = (
                'Could not obtain access token from Facebook. Check your'
                ' settings for FACEBOOK_APP_ID and FACEBOOK_APP_SECRET')
        super(AccessTokenException, self).__init__(message)


class FacebookLoginException(Exception):  # pragma: nocover
    """
    Raised when, despite all checks, we could authenticate the facebook_user.

    This should never happen.

    """
    def __init__(self, message=None):
        if message is None:
            message = (
                'Unable to authenticate facebook_user. This should never'
                ' happen.')
        super(FacebookLoginException, self).__init__(message)
