from __future__ import absolute_import

import logging
from enum import Enum
from typing import Callable

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from .const import locale
from .errors import OverwatchAPIError

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())
logger.setLevel(logging.DEBUG)

__version__: str = "0.0.2"


class EndPoint(Enum):
    domain: str = "overfast-api.tekrop.fr"
    scheme: str = "https"
    api_base: str = "{scheme}://{domain}/".format(scheme=scheme, domain=domain)
    player_url: str = api_base + "players"  # with query params
    all_player_data_url: str = api_base + "players/{battletag}"
    player_summary_url: str = api_base + "players/{battletag}/summary"
    player_stats_summary_url: str = api_base + "players/{battletag}/stats/summary"
    player_career_url: str = api_base + "players/{battletag}/stats/career"
    map_url: str = api_base + "maps"
    gamemodes_url: str = api_base + "gamemodes"
    heroes_url: str = api_base + "heroes"


class Client:
    """
    The main class for the Overwatch API wrapper
    """

    def __init__(
        self,
        use_retry: bool = True,
        timeout: int = 30,
    ) -> None:
        """
        Parameters
        ----------
        use_retry : bool
          default: True
          Whether to retry on HTTP status codes 500, 502, 503, 504
        timeout : int
          default: 30
          The timeout for the requests
        """
        self.session: requests.session = requests.session()
        self.session.headers["User-Agent"] = "overwatchpy/%s" % __version__
        self.session.headers["Accept"] = "application/json"
        self.timeout: int = timeout
        if use_retry:
            # Retry maximum 10 times, backoff on each retry
            # Sleeps 1s, 2s, 4s, 8s, etc to a maximum of 120s between retries
            # Retries on HTTP status codes 500, 502, 503, 504
            retries: Retry = Retry(
                total=10, backoff_factor=1, status_forcelist=[500, 502, 503, 504]
            )
            self.session.mount("https://", HTTPAdapter(max_retries=retries))

        self.local: list = locale

    def close(self):
        self.session.close()

    def request(
        self,
        path,
        method: str = "GET",
        params: dict = None,
        headers: dict = None,
        raw: bool = False,
        allow_redirects: bool = True,
        timeout: int = None,
    ) -> Callable[[dict], OverwatchAPIError]:
        """
        Wrapper around requests.request()

        Parameters
        ----------
        path : str
          The path
        method : str
          default: "GET"
          The HTTP method
        params : dict
          default: None
          The query parameters
        headers : dict
          default: None
          The headers
        raw : bool
          default: False
          Whether to return the raw response
        allow_redirects : bool
          default: True
          Whether to allow redirects
        timeout : int
          default: None
          The timeout for the request

        returns
        -------
        Callable[[dict], OverwatchAPIError]
        """
        if not headers:
            headers: dict = {}

        if not params:
            params: dict = {}

        if not timeout:
            timeout: int = self.timeout

        response = self.session.request(
            method,
            path,
            params=params,
            headers=headers,
            allow_redirects=allow_redirects,
            timeout=self.timeout,
        )
        logger.debug("Response: %s", response)
        if response.status_code != 200:
            raise OverwatchAPIError(response.status_code, response.text)

        if raw:
            return response

        return response.json()
