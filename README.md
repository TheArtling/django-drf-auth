# Django DRF Auth

EXPERIMENTAL! DO NOT USE THIS!

Authentication utilities for projects that use Django Rest Framework and
Facebook login.

[django-allauth](https://github.com/pennersr/django-allauth) is a fantastic
and very easy to extend library and you should probably use it. This library
will never be as thoroughly tested and as powerful as allauth.

However, we have found that we always need a few things on top of allauth and
we always end up hooking up so many third party apps and overriding various
settings/forms/classes, that "hooking up allauth" isn't really all that simple.

We usually need:

1. Authentication for normal web-forms.
1. Autentication against API endpoints for ReactJS components / mobile apps.
1. Facebook login.
1. Authentication via email, not username. Assumption: User.email is unique.
1. Making sure that we collect name & email if users blocked those access
   rights on Facebook.
1. Redirect to different pages after login depending on the user's status.
1. Redirect to different success pages after password reset / account
   verification.
1. Better hooks to track how a user authenticated.
1. Auth with JSON web tokens.
1. Good workflows for re-fetching long living Facebook tokens before they
   expire.
1. Being able to handle authentication status for several devices per user.

This app is an attempt to put everything that we need for theartling.com and
luxglove.com into one app. Hopefully this might turn out to be transferrable
to other projects and easy to setup.

EXPERIMENTAL! DO NOT USE THIS!


## Installation

To get the latest stable release from PyPi

To get the latest commit from GitHub

```bash
pip install -e git+git://github.com/TheArtling/django-drf-auth.git#egg=drf_auth
```

Add `drf_auth` to your `INSTALLED_APPS` setting:

```python
INSTALLED_APPS = (
    ...,
    'drf_auth',
)
```

Add `FinishSignupMiddleware` to your `MIDDLEWARE_CLASSES` setting:

```python
MIDDLEWARE = [
  ...
  'drf_auth.middleware.drf_auth_middleware.FinishSignupMiddleware',
]
```

Add the `drf_auth` URLs to your `urls.py`

```python
urlpatterns = [
    url(r'^auth/', include('drf_auth.urls')),
]
```

Don't forget to migrate your database:

```bash
./manage.py migrate drf_auth
```


## Contribute

If you want to contribute to this project, please perform the following steps

```bash
# Fork this repository
# Clone your fork
mkvirtualenv -p python2.7 django-drf-auth
pip install -r requirements.txt
pip install -r test_requirements.txt

git co -b feature_branch master
# Implement your feature and tests
git add . && git commit
git push -u origin feature_branch
# Send us a pull request for your feature branch
```

In order to run the tests, simply execute `./runtests.py`.
