#!/usr/bin/env python3

from typing import Dict
from bs4 import BeautifulSoup
import steam.webauth as wa


class SteamScraper:
    """
    A class to scrape Steam Workshop for subscribed addons.

    This class authenticates with Steam and retrieves information about
    subscribed workshop items for a specific app.
    """

    def __init__(self, *, userid: str, pw: str = '', mfa: str = '', prompt: bool = False, appid: str = '346110'):
        """
        Initialize the SteamScraper with authentication details.

        Args:
            userid: Steam username
            pw: Steam password (optional if using prompt)
            mfa: Two-factor authentication code (optional if using prompt)
            prompt: Whether to prompt for authentication interactively
            appid: The Steam Workshop App ID (default is Ark Survival Evolved)
        """
        self._app_id = appid
        self._user = wa.WebAuth(userid)
        self._user.steam_id_base = '76561197971835915'
        if prompt:
            self._session = self._user.cli_login()
        else:
            self._session = self._user.login(password=pw, twofactor_code=mfa)
        self._results: Dict[str, str] = {}

    def subscription_data(self) -> Dict[str, str]:
        """
        Connect to Steam URL and get the mod info scraped from the web page.

        Due to pagination, we loop until there are no more results.

        Returns:
            Dictionary mapping mod IDs to mod names
        """
        steam_url = self._parse_userid()
        page = 1
        while True:
            # Regardless of numberpage setting, always seems to get 10 at a time through API
            # base_url = f'{steam_url}/?appid={self._app_id}&browsefilter=mysubscriptions&p={page}&numberpage=30'
            base_url = f'{steam_url}&p={page}&numberpage=30'
            response = self._user.session.get(base_url)
            counter = self._parse_data(text=response.text)
            if counter == 0:
                break
            page += 1
        return self._results

    def _parse_userid(self) -> str:
        """
        Get the Steam ID URL for subscribed items.

        Steam requires the actual Steam ID (not just username) to get subscribed items.
        This method retrieves the correct URL with the Steam ID.

        Returns:
            The base URL with the proper Steam ID
        """
        # url = f'https://steamcommunity.com/id/{self._user.username}/myworkshopfiles/?appid={self._app_id}&browsefilter=mysubscriptions&p=1&numberpage=30'
        url = f'https://steamcommunity.com/id/{self._user.steam_id}/myworkshopfiles/?appid={self._app_id}&browsefilter=mysubscriptions'
        # url = 'https://steamcommunity.com/id/marakai666/myworkshopfiles/?appid=346110&browsefilter=mysubscriptions'
        # url = 'https://steamcommunity.com/id/76561197971835915/myworkshopfiles/?appid=346110&browsefilter=mysubscriptions'
        response = self._user.session.get(url)
        return response.url

    def _parse_data(self, *, text: str) -> int:
        """
        Parse the HTML data to extract workshop item information.

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