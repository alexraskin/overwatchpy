class OverwatchAPIError(Exception):
    """Base exception class for overwatchpy"""

    ...


class InvalidBattletag(Exception):
    """
    Raise when 'battletag' key word argument is none
    """

    ...


class InvalidGamemode(Exception):
    """
    Raise when 'gamemode' key word argument is not recognized
    """

    ...


class PlatformNotRecognized(Exception):
    """
    Raise when 'platform' key word argument is not recognized
    """

    ...


class InvalidPrivacySettings(Exception):
    """
    Raise when 'privacy' key word argument is not recognized
    """

    ...


class InvalidOrderBy(Exception):
    """
    Raise when 'order_by' key word argument is not recognized
    """

    ...
