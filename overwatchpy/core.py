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

from .objects import (
    OverwatchHeros,
    OverwatchHero,
    OverwatchMaps,
    OverwatchRole,
    OverwatchGameModes,
    OverwatchPlayerSearch,
    PlayerProfileSummary,
    OverwatchPlayerStats,
    AllPlayerStats,
)

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class Overwatch(Client):
    client = Client()

    def __init__(
        self,
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

    def format_battletag(self, battletag: str) -> str:
        """
        Formats the battletag

        Parameters
        ----------
        battletag : str
          The player's battletag

        returns
        -------
        str : str
        """
        return str(battletag).replace("#", "-")

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

    def player_search(
        self,
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
    ) -> Callable[[OverwatchPlayerSearch], OverwatchAPIError]:
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

        returns
        -------
        Callable[[OverwatchPlayerSearch], OverwatchAPIError]
        """
        if battletag is None:
            raise InvalidBattletag("Battletag is required")

        if not self.battle_tag_check(updated_battletag):
            raise InvalidBattletag("Invalid battletag")

        updated_battletag = self.format_battletag(battletag)

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
            "name": updated_battletag,
            "privacy": privacy,
            "platform": platform,
            "gamemode": gamemode,
            "order_by": order_by,
            "offset": offset,
            "limit": limit,
        }
        response = self.client.request(
            path=EndPoint.player_url.value, params=urlencode(params)
        )

        return [OverwatchPlayerSearch(response) for response in response]

    def ping(self) -> Callable[[dict], OverwatchAPIError]:
        """
        Returns the ping

        returns
        -------
        Callable[[dict], OverwatchAPIError]
        """
        return self.client.request(EndPoint.api_base.value)

    def player_summary(
        self, battletag: Optional[str] = None
    ) -> Callable[[PlayerProfileSummary], OverwatchAPIError]:
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
        if battletag is None:
            raise InvalidBattletag("Battletag is required")

        if self.battle_tag_check(battletag):
            raise InvalidBattletag("Invalid battletag")

        updated_battletag = self.format_battletag(battletag)

        response = self.client.request(
            EndPoint.player_summary_url.value.format(battletag=updated_battletag)
        )
        return PlayerProfileSummary(**response)

    def all_player_data(
        self, battletag: Optional[str] = None
    ) -> Callable[[AllPlayerStats], OverwatchAPIError]:
        """
        Returns the player's all data

        Parameters
        ----------
        battletag : str
          The player's battletag

        returns
        -------
        Callable[[AllPlayerStats], OverwatchAPIError]
        """
        if battletag is None:
            raise InvalidBattletag("Battletag is required")

        print(self.battle_tag_check(battletag))

        if not self.battle_tag_check(battletag):
            raise InvalidBattletag("Invalid battletag")

        updated_battletag = self.format_battletag(battletag)

        response = self.client.request(
            EndPoint.domain.all_player_data_url.value.format(
                battletag=updated_battletag
            )
        )
        return AllPlayerStats.parse(data=response)

    def player_stats(
        self,
        battletag: Optional[str] = None,
        gamemode: Optional[Literal["quickplay", "competitive"]] = None,
        platform: Optional[Literal["pc", "console"]] = None,
    ) -> Callable[[OverwatchPlayerStats], OverwatchAPIError]:
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
        if battletag is None:
            raise InvalidBattletag("Battletag is required")

        if not self.battle_tag_check(battletag):
            raise InvalidBattletag("Invalid battletag")

        updated_battletag = self.format_battletag(battletag)

        if gamemode is None:
            raise InvalidGamemode("Gamemode is required")
        if platform is None:
            raise PlatformNotRecognized("Platform is required")
        params = {
            "gamemode": gamemode,
            "platform": platform,
        }
        response = self.client.request(
            EndPoint.player_stats_summary_url.value.format(battletag=updated_battletag),
            params=urlencode(params),
        )
        return OverwatchPlayerStats(**response)

    def player_career(
        self,
        hero: Optional[str] = "all-heros",
        battletag: Optional[str] = None,
        gamemode: Optional[Literal["quickplay", "competitive"]] = None,
        platform: Optional[Literal["pc", "console"]] = None,
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
        if battletag is None:
            raise InvalidBattletag("Battletag is required")

        if not self.battle_tag_check(battletag):
            raise InvalidBattletag("Invalid battletag")

        updated_battletag = self.format_battletag(battletag)

        if gamemode is None:
            raise InvalidGamemode("Gamemode is required")
        if platform is None:
            raise PlatformNotRecognized("Platform is required")
        params = {
            "gamemode": gamemode,
            "platform": platform,
            "hero": "all-heroes" if hero is None else hero,
        }
        return self.client.request(
            EndPoint.player_career_url.value.format(battletag=updated_battletag),
            params=urlencode(params),
        )

    def roles(self) -> Callable[[OverwatchRole], OverwatchAPIError]:
        """
        Returns the roles

        returns
        -------
        Callable[[dict], OverwatchAPIError]
        """
        response = self.client.request(EndPoint.roles_url.value)
        return [OverwatchRole(**response) for response in response]

    def maps(self) -> Callable[[OverwatchMaps], OverwatchAPIError]:
        """
        Returns the maps

        returns
        -------
        Callable[[dict], OverwatchAPIError]
        """
        response = self.client.request(EndPoint.map_url.value)
        return [OverwatchMaps(**response) for response in response]

    def gamemodes(self) -> Callable[[OverwatchGameModes], OverwatchAPIError]:
        """
        Returns the gamemodes
        """
        response = self.client.request(EndPoint.gamemodes_url.value)
        return [OverwatchGameModes(**response) for response in response]

    def heroes(
        self,
        role: Literal["damage", "support", "tank"] = None,
        locale: Optional[str] = "en-us",
    ) -> Callable[[OverwatchHeros], OverwatchAPIError]:
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
        params = {
            "locale": locale if locale in self.local else "en-us",
        }
        if role is not None:
            params["role"] = role
            if role not in ["damage", "support", "tank"]:
                raise InvalidGamemode("Role must be either 'damage', 'support', 'tank'")
        response = self.client.request(
            EndPoint.heroes_url.value, params=urlencode(params)
        )
        return [OverwatchHeros(**response) for response in response]

    def hero(
        self,
        hero: str,
        locale: Optional[str] = "en-us",
    ) -> Callable[[OverwatchHero], OverwatchAPIError]:
        """
        Returns the hero

        Parameters
        ----------
        hero : str
          The hero
        locale : str
          The locale (default: en-us)

        returns
        -------
        Callable[[OverwatchHero], OverwatchAPIError]
        """
        params = {
            "locale": locale if locale in self.local else "en-us",
        }
        if hero is None:
            raise InvalidGamemode("Hero is required")
        response = self.client.request(
            EndPoint.hero_url.value.format(hero=hero), params=urlencode(params)
        )
        return OverwatchHero(**response)
