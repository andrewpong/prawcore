"""Provides the HTTP request handling interface."""
import requests
from .const import __version__
from .exceptions import InvalidInvocation


class Requestor(object):
    """Requestor provides an interface to HTTP requests."""

    def __init__(self, user_agent):
        """Create an instance of the Requestor class.

        :param user_agent: The user-agent for your application. Please follow
            reddit's user-agent guidlines:
            https://github.com/reddit/reddit/wiki/API#rules

        """
        if user_agent is None or len(user_agent) < 7:
            raise InvalidInvocation('user_agent is not descriptive')

        self._http = requests.Session()
        self._http.headers['User-Agent'] = '{} prawcore/{}'.format(
            user_agent, __version__)

    def __getattr__(self, attribute):
        """Pass all undefined attributes to the _http attribute."""
        return getattr(self._http, attribute)
