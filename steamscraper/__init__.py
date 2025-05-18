from steamscraper.steamapi import Scraper
from importlib.metadata import version as get_version

try:
    __version__ = get_version("steamscraper")
except Exception:
    __version__ = "unknown"

__all__ = ["Scraper", "__version__"]
