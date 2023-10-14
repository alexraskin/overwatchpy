from typing import Literal, Optional, Dict, Callable, Any, List


class BaseClass:
    def __init__(self) -> None:
        ...

class Ping(BaseClass):
    def __init__(self, ping: int) -> None:
        super().__init__()
        self.ping: int = ping

    def __str__(self) -> str:
        return f"Ping: {self.ping}"

class OverwatchHeros(BaseClass):
    def __init__(self, key: str, name: str, portrait: str, role: str):
        super().__init__()
        self.key: str = key
        self.name: str = name
        self.portrait: str = portrait
        self.role: str = role

    def __str__(self) -> str:
        return f"Hero: {self.name}\nRole: {self.role}\nKey: {self.key}\nPortrait: {self.portrait}"


class OverwatchHero:
    def __init__(
        self,
        name: str,
        description: str,
        portrait: str,
        role: str,
        location: str,
        hitpoints: Dict[str, int],
        abilities: List[Dict[str, Any]],
        story: Dict[str, Any],
    ):
        super().__init__()
        self.name: str = name
        self.description: str = description
        self.portrait: str = portrait
        self.role: str = role
        self.location: str = location
        self.hitpoints: Dict[str, int] = hitpoints
        self.abilities: List[Dict[str, Any]] = abilities
        self.story: Dict[str, Any] = story

    def __str__(self) -> str:
        return f"Hero: {self.name}\nRole: {self.role}\nLocation: {self.location}\nPortrait: {self.portrait}\nDescription: {self.description}\nHitpoints: {self.hitpoints}\nAbilities: {self.abilities}\nStory: {self.story}"


class OverwatchRole(BaseClass):
    def __init__(self, key: str, name: str, icon: str, description: str):
        super().__init__()
        self.key: str = key
        self.name: str = name
        self.icon: str = icon
        self.description: str = description

    def __str__(self) -> str:
        return f"Role: {self.name}\nKey: {self.key}\nIcon: {self.icon}\nDescription: {self.description}"


class OverwatchMaps(BaseClass):
    def __init__(
        self,
        name: str,
        screenshot: str,
        gamemodes: List[str],
        location: str,
        country_code: Optional[str],
    ):
        super().__init__()
        self.name: str = name
        self.screenshot: str = screenshot
        self.gamemodes: List = gamemodes
        self.location: str = location
        self.country_code: str = country_code

    def __str__(self) -> str:
        return f"Map: {self.name}\nLocation: {self.location}\nGamemodes: {', '.join(self.gamemodes)}\nCountry Code: {self.country_code}\nScreenshot: {self.screenshot}"


class OverwatchGameModes(BaseClass):
    def __init__(
        self, key: str, name: str, icon: str, description: str, screenshot: str
    ):
        super().__init__()
        self.key: str = key
        self.name: str = name
        self.icon: str = icon
        self.description: str = description
        self.screenshot: str = screenshot

    def __str__(self) -> str:
        return f"Game Mode: {self.name}\nKey: {self.key}\nIcon: {self.icon}\nDescription: {self.description}\nScreenshot: {self.screenshot}"


class OverwatchPlayerSearch(BaseClass):
    def __init__(self, total: int, results: List[Dict[str, str]]):
        super().__init__()
        self.total: int = total
        self.results: List[Dict[str, str]] = results

    def __str__(self) -> str:
        return f"Total Results: {self.total}\nResults: {self.results}"


class PlayerProfileSummary(BaseClass):
    def __init__(
        self,
        username: str,
        avatar: str,
        namecard: str,
        title: str,
        endorsement: Dict[str, str],
        competitive: Dict[str, Dict[str, Any]],
        privacy: str,
    ):  
        super().__init__()
        self.username: str = username
        self.avatar: str = avatar
        self.namecard: str = namecard
        self.title: str = title
        self.endorsement: Dict[str, str] = endorsement
        self.competitive: Dict[str, Dict[str, Any]] = competitive
        self.privacy: str = privacy

    def __str__(self) -> str:
        return f"Username: {self.username}\nAvatar: {self.avatar}\nNamecard: {self.namecard}\nTitle: {self.title}\nEndorsement: {self.endorsement}\nCompetitive: {self.competitive}\nPrivacy: {self.privacy}"


class OverwatchPlayerStats(BaseClass):
    def __init__(self, data: Dict[str, Any]) -> None:
        super().__init__()
        self.general = self.GeneralStats(data["general"])
        self.heroes = {hero: self.HeroStats(stats) for hero, stats in data["heroes"].items()}
        self.roles = {role: self.RoleStats(stats) for role, stats in data["roles"].items()}

    class OverwatchGeneralStats:
        def __init__(self, data: Dict[str, Any]) -> None:
            self.average = data["average"]
            self.games_lost = data["games_lost"]
            self.games_played = data["games_played"]
            self.games_won = data["games_won"]
            self.kda = data["kda"]
            self.time_played = data["time_played"]
            self.total = data["total"]
            self.winrate = data["winrate"]

    class OverwatchHeroStats:
        def __init__(self, data: Dict[str, Any]) -> None:
            self.average = data["average"]
            self.games_lost = data["games_lost"]
            self.games_played = data["games_played"]
            self.games_won = data["games_won"]
            self.kda = data["kda"]
            self.time_played = data["time_played"]
            self.total = data["total"]
            self.winrate = data["winrate"]

    class OverwatchRoleStats:
        def __init__(self, data: Dict[str, Any]) -> None:
            self.average = data["average"]
            self.games_lost = data["games_lost"]
            self.games_played = data["games_played"]
            self.games_won = data["games_won"]
            self.kda = data["kda"]
            self.time_played = data["time_played"]
            self.total = data["total"]
            self.winrate = data["winrate"]
