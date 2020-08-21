import functools
from urllib.parse import urljoin

from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings

from requests_oauthlib import OAuth2Session

TOKEN_SESSION_KEY = settings.TOKEN_SESSION_KEY
PROFILE_URL = urljoin(settings.AUTHBROKER_URL, "/api/v1/user/me/")
INTROSPECT_URL = urljoin(settings.AUTHBROKER_URL, "o/introspect/")
TOKEN_URL = urljoin(settings.AUTHBROKER_URL, "/o/token/")
AUTHORISATION_URL = urljoin(settings.AUTHBROKER_URL, "/o/authorize/")
TOKEN_CHECK_PERIOD_SECONDS = 60
SCOPE = "read write"


def get_client(request, **kwargs):
    redirect_uri = request.build_absolute_uri(reverse("auth:callback"))

    return OAuth2Session(
        settings.AUTHBROKER_CLIENT_ID,
        redirect_uri=redirect_uri,
        scope=SCOPE,
        token=request.session.get(TOKEN_SESSION_KEY, None),
        **kwargs,
    )


def get_profile(client):
    response = client.get(PROFILE_URL)  # .json()
    return response.json()


def authbroker_login_required(func):
    """Check that the current session has authenticated with the authbroker and has a valid token.
    This is different to the @login_required decorator in that it only checks for a valid authbroker Oauth2 token,
    not an authenticated django user."""

    @functools.wraps(func)
    def decorated(request):
        if not get_client(request).authorized:
            return redirect("auth:login")

        return func(request)

    return decorated
