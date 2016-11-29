# Django DRF Auth

EXPERIMENTAL! DO NOT USE THIS!

Authentication utilities for projects that use Django Rest Framework and
Facebook login.

[django-allauth](https://github.com/pennersr/django-allauth) is a fantastic
and very easy to extend library and you should probably use it. This library
will never be as thoroughly tested and as powerful as allauth.

However, we have found that we usually need a few things on top of allauth and
end up hooking up various third party apps and override various
settings/forms/classes. In the end, "just using allauth" isn't really all that simple any more.

Unfortunately, our web apps are currently hybrid apps where some parts are
"old school" Django views that rely on session based authentication. Therefore
we simply send our AJAX requests from our ReactJS apps with
`withCredentials: true` and we re-use the session based authentication that was
already set by Django. Our mobile apps, on the other hand, don't rely on
session based authentication and should use JSON Web Tokens.

We usually need:

1. Authentication for normal web-forms.
1. Authentication against API endpoints for session based auth for ReactJS
   components / mobile apps.
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

Add `EmailAuthenticationBackend` and `FacebookAuthenticationBackend` to your
`AUTHENTICATION_BACKENDS` setting:

```python
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "drf_auth.auth_backends.EmailAuthenticationBackend",
    "drf_auth.auth_backends.FacebookAuthenticationBackend",
)
```

Add the `drf_auth` URLs to your `urls.py`

```python
urlpatterns = [
    url(r'^auth/', include('drf_auth.urls')),
]
```

You are probably hooking up your API urls under a different path, so hook
up the `drf_auth` API-URLs as well (probably in your `api_urls.py`):

```python
# In your main urls.py you might have something like this:
urlpatterns = [
    url(r'^api/(?P<version>v1)/', include('project.api_urls')),
]

# In your main api_urls.py you can then add this:
urlpatterns = [
    url(r'^auth/$', include('drf_auth.api_urls')),
]
```

Don't forget to migrate your database:

```bash
./manage.py migrate drf_auth
```


## Usage

In your `base.html` you need to place a container into which we can render the
ReactJS-based `AuthContainer` component. Our component is designed to slide in:
from the top, so you should put it at the very top of your `body` tag.

```html
<body style="margin: 0px;">
  <div id="authApp"></div>
  <!-- ... header of your website -->
  <div onclick="drfAuthLoginClicked();">Login</div>
  <div onclick="drfAuthSignupClicked();">Signup</div>
  <!-- ... rest of your base.html content -->
  <script type="text/javascript" src="{% static "path/to/your/react/lib/"%}"></script>
  <script type="text/javascript" src="{% static "drf_auth/AuthApp.js" %}"></script>
  <script type="text/javascript" src="{% static "drf_auth/init.js" %}"></script>
</body>
```

When you load `drf_auth/init.js` it registers a globally available function
`drfAuthLoginClicked()` which emits a CustomEvent. The react component listens
to that event and slides in when the event happens.


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

In order to run the test project, make sure to create copies of
`local_settings.py.sample` and `webpack.local_settings.js` and change the
relevant values in those files.

In order to run the webpack-dev-server, run `npm install` and run
`node server.js`.

In order to run the local development server, run
`./manage.py runserver IP:8000`
