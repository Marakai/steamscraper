#!/usr/bin/env python3

import steam.webauth as wa
from typing import Dict
from bs4 import BeautifulSoup
from steamscraper.config import ScraperConfig
from steamscraper.steamapi.steamguard import get_steamguard_code


class Scraper:
    """A class to scrape Steam Workshop for subscribed addons.
    Authenticates with Steam and retrieves information about subscribed workshop items."""

    def __init__(self, config: ScraperConfig):
        """Initialize the Scraper with configuration.
        Args:
            config: ScraperConfig object containing authentication details and settings
        """

        self._config = config
        self._user = wa.WebAuth(config.steamlogin)
        self._user.steam_id_base = config.steamid
        self._session = self._user.login(password=config.password, twofactor_code=get_steamguard_code())

        self._results: Dict[str, str] = {}

    def subscription_data(self) -> Dict[str, str]:
        """Connect to Steam URL and get the mod info scraped from the web page.
        Due to pagination, we loop until there are no more results.
        Returns:
            Dictionary mapping mod IDs to mod names
        """

        url_steamid = f'https://steamcommunity.com/id/{self._config.steamid}/myworkshopfiles/?appid={self._config.appid}&browsefilter=mysubscriptions'
        url_username = f'https://steamcommunity.com/id/{self._config.username}/myworkshopfiles/?appid={self._config.appid}&browsefilter=mysubscriptions'

        self._parse_loop(url_steamid)
        self._parse_loop(url_username)
        return self._results

    def _parse_loop(self, url: str) -> int:
        page = 1
        while True:
            work_url = f'{url}&p={page}'
            response = self._session.get(work_url)
            counter = self._parse_data(text=response.text)
            if counter == 0:
                break
            page += 1
        return counter

    def _parse_data(self, *, text: str) -> int:
        """Parse the HTML data to extract workshop item information.
        Args:
            text: The raw HTML data from the Steam Workshop page
        Returns:
            Number of entries found (0 indicates no more results)
        """
        soup = BeautifulSoup(text, 'html.parser')
        div_entries = soup.find_all('div', class_='itemContents')
        if not div_entries:
            return 0

        for addon_entry in div_entries:
            addon_id = addon_entry.find('a').attrs.get('href').split('=')[1]
            title = addon_entry.find('div', {'class': 'workshopItemTitle'}).text
            self._results[addon_id] = title

        return len(div_entries)
