"""Provides Authentication and Authorization classes."""

import requests
import time
from . import const
from .exceptions import InvalidInvocation


class Authenticator(object):
    """Stores OAuth2 authentication credentials."""

    def __init__(self, client_id, client_secret):
        """Represent a single authentication to reddit's API.

        :param client_id: The OAuth2 client id to use with the session.
        :param client_secret: The OAuth2 client secret to use with the session.

        """
        self.client_id = client_id
        self.client_secret = client_secret


class Authorizer(object):
    """Manages OAuth2 authorization tokens and scopes."""

    def __init__(self, authenticator, refresh_token=None):
        """Represent a single authorization to reddit's API.

        :param authenticator: An instance of :class:`Authenticator`.
        :param refresh_token: (Optional) Enables the ability to refresh the
            authorization.

        """
        self.authenticator = authenticator
        self.access_token = None
        self.expiration = None
        self.refresh_token = refresh_token
        self.scopes = None

    def refresh(self):
        """Obtain a new access token from the refresh_token."""
        if self.refresh_token is None:
            raise InvalidInvocation('refresh token not provided')
        auth = (self.authenticator.client_id, self.authenticator.client_secret)
        data = {'grant_type': 'refresh_token',
                'refresh_token': self.refresh_token}
        try:
            data = requests.post(
                const.ACCESS_TOKEN_URL, auth=auth, data=data,
                headers={'User-Agent': const.USER_AGENT}).json()
        except:
            raise

        self.access_token = data['access_token']
        self.expiration = time.time() + data['expires_in']
        self.scopes = set(data['scope'].split(' '))
