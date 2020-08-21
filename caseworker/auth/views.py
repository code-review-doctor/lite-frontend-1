import logging

import sentry_sdk

from django.http import HttpResponseBadRequest, HttpResponseServerError
from django.shortcuts import redirect
from django.views.generic.base import View

from caseworker.auth.services import authenticate_gov_user
from caseworker.auth.utils import get_client, AUTHORISATION_URL, TOKEN_SESSION_KEY, TOKEN_URL, get_profile
from django.conf import settings
from lite_content.lite_internal_frontend import strings
from lite_forms.generators import error_page
from core.auth import views as auth_views


class AuthView(auth_views.AuthView):

    TOKEN_SESSION_KEY = TOKEN_SESSION_KEY
    AUTHORIZATION_URL = AUTHORISATION_URL

    def get_client(self):
        return get_client(self.request)


class AuthCallbackView(View):
    def get(self, request, *args, **kwargs):
        logging.info("Login callback received from Staff SSO")

        auth_code = request.GET.get("code", None)

        if not auth_code:
            return HttpResponseBadRequest()

        state = self.request.session.get(TOKEN_SESSION_KEY + "_oauth_state", None)

        if not state:
            return HttpResponseServerError()

        try:
            token = get_client(self.request).fetch_token(
                TOKEN_URL, client_secret=settings.AUTHBROKER_CLIENT_SECRET, code=auth_code
            )

            self.request.session[TOKEN_SESSION_KEY] = dict(token)

            del self.request.session[TOKEN_SESSION_KEY + "_oauth_state"]

        # NOTE: the BaseException will be removed or narrowed at a later date. The try/except block is
        # here due to reports of the app raising a 500 if the url is copied.  Current theory is that
        # somehow the url with the authcode is being copied, which would cause `fetch_token` to raise
        # an exception. However, looking at the fetch_code method, I'm not entirely sure what exceptions it
        # would raise in this instance.
        except BaseException as base_exception:
            sentry_sdk.capture_exception(base_exception)

        profile = get_profile(get_client(self.request))

        response, status_code = authenticate_gov_user(request, profile)
        if status_code != 200:
            return error_page(
                None,
                title=strings.Authentication.UserDoesNotExist.TITLE,
                description=strings.Authentication.UserDoesNotExist.DESCRIPTION,
                show_back_link=False,
            )

        request.session["first_name"] = profile["first_name"]
        request.session["last_name"] = profile["last_name"]

        request.session["default_queue"] = response["default_queue"]
        request.session["user_token"] = response["token"]
        request.session["lite_api_user_id"] = response["lite_api_user_id"]
        request.session.save()

        return redirect(getattr(settings, "LOGIN_REDIRECT_URL", "/"))