import asyncio
import datetime
import inspect
import re
import sys
import webbrowser

import grpc
from google.protobuf.empty_pb2 import Empty

import ai.h2o.featurestore.api.v1.CoreService_pb2 as pb
from featurestore.core.config import ConfigUtils

from .collections.pats import PersonalAccessTokens


class AuthWrapper:
    ACCESS_TOKEN_EXPIRES_SOON_SECS = 60

    def __init__(self, stub):
        self._stub = stub
        self._access_token = None
        self._access_token_expiration_date = None
        self._get_access_token_external = None
        self._props = ConfigUtils.collect_properties()
        self.pats = PersonalAccessTokens(self._stub)

    def get_active_user(self):
        request = Empty()
        return self._stub.GetActiveUser(request).user

    def set_obtain_access_token_method(self, method):
        self._get_access_token_external = method

    def logout(self):
        is_success, token_or_error = self._obtain_token()
        if is_success:
            if not AuthWrapper._is_personal_access_token(self._props["token"].data):
                request = pb.LogoutRequest()
                request.refresh_token = self._props["token"].data
                self._stub.Logout(request)
                self._access_token = None
                self._access_token_expiration_date = None
            ConfigUtils.delete_property(self._props, ConfigUtils.TOKEN_KEY)
            print("You have been logged out.")
        else:
            print("You are not logged in.")

    def login(self, open_browser=True):
        try:
            sys.tracebacklimit = None
            for response in self._stub.Login(Empty()):
                if response.HasField("login_url"):
                    if open_browser:
                        try:
                            webbrowser.get()
                            webbrowser.open(response.login_url)
                            print(f"Opening browser to visit: {response.login_url}")
                        except webbrowser.Error:
                            print(
                                f"Browser is not supported: Please visit "
                                f"{response.login_url} to continue authentication."
                            )
                    else:
                        print(f"Please visit {response.login_url} to continue authentication.")
                elif response.HasField("refresh_token"):
                    self.set_auth_token(response.refresh_token)
                else:
                    sys.tracebacklimit = 0
                    raise AuthException("Incorrect response")
        except grpc._channel._MultiThreadedRendezvous:
            print("Your logging session expired, please login again by running client.auth.login().")

    def set_auth_token(self, token):
        sys.tracebacklimit = None
        ConfigUtils.store_token(self._props, token)
        if not AuthWrapper._is_personal_access_token(token):
            self._access_token = None
            self._access_token_expiration_date = None
            is_success, token_or_error = self._obtain_token()
            if not is_success:
                sys.tracebacklimit = 0
                raise AuthException(token_or_error)

    @staticmethod
    def _is_personal_access_token(token: str) -> bool:
        return re.match(r"^[a-z0-9]{3}_.*", token)

    def _is_access_token_expired(self):
        if not self._access_token:
            return True
        if self._access_token_expiration_date is not None:
            expires_in = (self._access_token_expiration_date - datetime.datetime.now()).total_seconds()
            return expires_in <= AuthWrapper.ACCESS_TOKEN_EXPIRES_SOON_SECS

        return False

    def _obtain_token(self):
        if self._get_access_token_external is not None:
            external_token = self._get_access_token_external()
            if inspect.isawaitable(external_token):
                loop = asyncio.get_event_loop()
                return True, loop.run_until_complete(external_token)
            else:
                return True, external_token
        elif ConfigUtils.TOKEN_KEY not in self._props:
            return (
                False,
                "You are not authenticated. Set personal access token or execute client.auth.login() method",
            )
        elif AuthWrapper._is_personal_access_token(ConfigUtils.get_token(self._props)):
            return True, ConfigUtils.get_token(self._props)
        elif self._is_access_token_expired():
            request = pb.RefreshTokenRequest()
            request.refresh_token = ConfigUtils.get_token(self._props)
            try:
                resp = self._stub.GetAccessToken(request)
            except grpc.RpcError:
                return (
                    False,
                    "The authentication token is no longer valid. Please login again.",
                )

            self._access_token = resp.access_token
            ConfigUtils.store_token(self._props, resp.refresh_token)
            self._access_token_expiration_date = datetime.datetime.now() + datetime.timedelta(seconds=resp.expires_in)
            return True, self._access_token
        else:
            return True, self._access_token

    def __repr__(self):
        return "This class wraps together methods related to Authentication"


class AuthException(Exception):
    pass
