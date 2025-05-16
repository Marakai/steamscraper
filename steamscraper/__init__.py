from steamscraper.steamapi import SteamScraper
from importlib.metadata import version as get_version

try:
    __version__ = get_version("steamscraper")
except Exception:
    __version__ = "unknown"

__all__ = ["SteamScraper", "__version__"]
