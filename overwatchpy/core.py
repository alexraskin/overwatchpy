from __future__ import absolute_import

import logging
import re
from typing import Callable, Literal, Optional

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

from .api import Client, EndPoint
from .errors import (
    InvalidBattletag,
    InvalidGamemode,
    InvalidOrderBy,
    InvalidPrivacySettings,
    OverwatchAPIError,
    PlatformNotRecognized,
)

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

__version__ = "0.0.1"


class Overwatch(Client):
    client = Client()

    def __init__(
        self,
        battletag: str = None,
        gamemode: Literal["quickplay", "competitive"] = None,
        platform: Literal["pc", "console"] = None,
        _data: Optional[dict] = None,
    ) -> None:
        """
        Parameters
        ----------
        battletag : str
          The player's battletag
        gamemode : str
          The gamemode
        platform : str
          The platform
        _data : dict
          The data from the API
        """
        super().__init__()
        self.battletag = battletag
        self.gamemode = gamemode
        self.platform = platform
        if _data is not None:
            self._data = _data
            self.battletag = _data.get("player_id")
            self.privacy = _data.get("privacy")
            self.name = _data.get("name")

    def battle_tag_check(self, battletag: str) -> bool:
        """
        Checks if the battletag is valid

        Parameters
        ----------
        battletag : str
          The player's battletag
        
        returns
        -------
        bool : bool
        """
        reg = r"^[a-zA-Z0-9]{3,12}#[0-9]{4,5}$"
        return bool(re.match(reg, battletag))

    def ping(self) -> Callable[[dict], OverwatchAPIError]:
        """
        Returns the ping

        returns
        -------
        Callable[[dict], OverwatchAPIError]
        """
        return self.client.request(EndPoint.api_base.value)

    @classmethod
    def player_search(
        cls,
        battletag: str,
        gamemode: Literal["quickplay", "competitive"],
        platform: Literal["pc", "console"],
        privacy: Literal["public", "private"],
        order_by: Optional[
            Literal[
                "player_id:asc",
                "player_id:desc",
                "name:asc",
                "name:desc",
                "privacy:asc",
                "privacy:desc",
            ]
        ] = "name:asc",
        offset: Optional[int] = 0,
        limit: Optional[int] = 20,
    ) -> Callable[[dict], OverwatchAPIError]:
        """
        Search for a player

        Parameters
        ----------
        battletag : str
          The player's battletag
        gamemode : str
          The gamemode
        platform : str
          The platform
        privacy : str
          The privacy settings
        order_by : str
          The order by
        offset : int
          The offset
        limit : int
          The limit
        """
        if not cls.battle_tag_check(battletag):
            raise InvalidBattletag("Invalid battletag")

        if privacy not in ["public", "private"]:
            raise InvalidPrivacySettings("Privacy must be either 'public', 'private'")

        if platform not in ["pc", "console"]:
            raise PlatformNotRecognized("Platform must be either 'pc', 'console'")

        if gamemode not in ["quickplay", "competitive"]:
            raise InvalidGamemode("Gamemode must be either 'quickplay', 'competitive'")

        if order_by not in [
            "player_id:asc",
            "player_id:desc",
            "name:asc",
            "name:desc",
            "privacy:asc",
            "privacy:desc",
        ]:
            raise InvalidOrderBy(
                "Order by must be either 'player_id:asc', 'player_id:desc', 'name:asc', 'name:desc', 'privacy:asc', 'privacy:desc'"
            )
        params = {
            "name": battletag,
            "privacy": privacy,
            "platform": platform,
            "gamemode": gamemode,
            "order_by": order_by,
            "offset": offset,
            "limit": limit,
        }
        response = cls.client.request(
            path=EndPoint.player_url.value, params=urlencode(params)
        )

        return [cls(_data=data) for data in response["results"]]

    def player_summary(
        self, battletag: Optional[str] = None
    ) -> Callable[[dict], OverwatchAPIError]:
        """
        Returns the player's summary

        Parameters
        ----------
        battletag : str
          The player's battletag
        
        returns
        -------
        Callable[[dict], OverwatchAPIError]
        """
        if self.battle_tag_check(battletag):
            raise InvalidBattletag("Invalid battletag")
        if battletag is None:
            battletag = self.battletag
        return self.client.request(
            EndPoint.player_summary_url.value.format(battletag=battletag)
        )

    def player_all_data(
        self, battletag: Optional[str] = None
    ) -> Callable[[dict], OverwatchAPIError]:
        """
        Returns the player's all data

        Parameters
        ----------
        battletag : str
          The player's battletag
        
        returns
        -------
        Callable[[dict], OverwatchAPIError]
        """
        if self.battle_tag_check(battletag):
            raise InvalidBattletag("Invalid battletag")
        if battletag is None:
            battletag = self.battletag
        return self.client.request(
            EndPoint.domain.all_player_data_url.value.format(battletag=self.battletag)
        )

    def player_stats(
        self,
        battletag: Optional[str] = None,
        gamemode: Optional[Literal] = None,
        platform: Optional[Literal["pc", "console"]] = None,
    ) -> Callable[[dict], OverwatchAPIError]:
        """
        Returns the player's stats

        Parameters
        ----------
        battletag : str
          The player's battletag
        gamemode : str
          The gamemode
        platform : str
          The platform
        
        returns
        -------
        Callable[[dict], OverwatchAPIError]
        """
        if self.battle_tag_check(battletag):
            raise InvalidBattletag("Invalid battletag")
        if battletag is None:
            battletag = self.battletag
        if gamemode is None:
            gamemode = self.gamemode
        if platform is None:
            platform = self.platform
        params = {
            "gamemode": gamemode,
            "platform": platform,
        }
        return self.client.request(
            EndPoint.player_stats_summary_url.value.format(battletag=battletag),
            params=urlencode(params),
        )

    def player_career(
        self,
        hero: Optional[Literal["all-heros"]] = "all-heros",
        battletag: Optional[str] = None,
        gamemode: Optional[str] = None,
        platform: Optional[str] = "pc",
    ) -> Callable[[dict], OverwatchAPIError]:
        """
        Returns the player's career

        Parameters
        ----------
        hero : str
          The hero
        battletag : str
          The player's battletag
        gamemode : str
          The gamemode
        platform : str
          The platform
        
        returns
        -------
        Callable[[dict], OverwatchAPIError]
        """
        if self.battle_tag_check(battletag):
            raise InvalidBattletag("Invalid battletag")
        if battletag is None:
            battletag = self.battletag
        if gamemode is None:
            gamemode = self.gamemode
        if platform is None:
            platform = self.platform
        params = {
            "gamemode": gamemode,
            "platform": platform,
            "hero": "all-heroes" if hero is None else hero,
        }
        return self.client.request(
            EndPoint.player_career_url.value.format(battletag=battletag),
            params=urlencode(params),
        )

    def maps(self) -> Callable[[dict], OverwatchAPIError]:
        """
        Returns the maps

        returns
        -------
        Callable[[dict], OverwatchAPIError]
        """
        return self.client.request(EndPoint.map_url.value)

    def gamemodes(self) -> Callable[[dict], OverwatchAPIError]:
        """
        Returns the gamemodes
        """
        return self.client.request(EndPoint.gamemodes_url.value)

    def heroes(
        self,
        role: Literal["damage", "support", "tank"],
        locale: Optional[str] = "en-us",
    ) -> Callable[[dict], OverwatchAPIError]:
        """
        Returns the heroes

        Parameters
        ----------
        role : str
          The role
        locale : str
          The locale (default: en-us)
        
        returns
        -------
        Callable[[dict], OverwatchAPIError]
        """
        if role not in ["damage", "support", "tank"]:
            raise InvalidGamemode("Role must be either 'damage', 'support', 'tank'")
        params = {
            "role": role,
            "locale": locale if locale in self.local else "en-us",
        }
        return self.client.request(EndPoint.heroes_url.value, params=urlencode(params))
