#!/usr/bin/env python3

from bs4 import BeautifulSoup
import steam.webauth as wa


class SteamScraper:
    def __init__(self, *, username: str, pw: str = '', mfa: str = '', prompt: bool = False, appid: str = '346110'):
        self._arksurvival_app_id = appid
        self._user = wa.WebAuth(username)
        if prompt:
            self._session = self._user.cli_login()
        else:
            self._session = self._user.login(password=pw, twofactor_code=mfa)
        self._results = {}

    def get_data(self) -> dict:
        """
        Connect to Steam URL and get the mod info scraped out of the raw web page.
        Due to this coming paginated, we loop until there's no more results.

        NOTE: the website supposedly allows paging with 30 items at a time, but for some reason it only ever
        gives the minimum of 10 at a time.

        :return: Dictionary of mod name and ID
        """
        steam_url = self.parse_userid()
        page = 1
        while True:
            # regardless of numberpage setting, always seem to get 10 at a time through API
            base_url = f'{steam_url}/?appid={self._arksurvival_app_id}&browsefilter=mysubscriptions&p={str(page)}&numberpage=30'
            rawdata = self._user.session.get(base_url)
            rawtext = rawdata.text
            counter = self.parse_data(text=rawtext)
            if counter == 0:
                break
            page += 1
        return self._results

    def parse_userid(self) -> str:
        """
        It seems you have to use the Steam ID to get subscribed items, NOT the mere username.
        So, first you have to get the URL, which it fill in itself, then do it all with THAT URL.

        For some reason, despite testing, we had to use a full query URL with the *username* and
        only then do we get the correct base URL with the Steam ID.

        :param url: The start URL from which to get the actual URL with ID
        :return: The base URL with the proper Steam ID
        """
        url = f'https://steamcommunity.com/id/{self._user.username}/myworkshopfiles/?appid={self._arksurvival_app_id}&browsefilter=mysubscriptions&p=1&numberpage=30'
        rawdata = self._user.session.get(url)
        return rawdata.url

    def parse_data(self, *, text: str) -> int:
        """
        Do the actual scraping magic with help of BeautifulSoup.
        The info we want is hidden in a div class called 'itemContents' (let's hope they don't change it).

        We stuff the key/value pairs of mod name and ID right into a class variable dict.

        :param text: The raw web data, one page at a time.
        :return: Number of entries found, when we get 0(zero) we know we're done.
        """
        soup = BeautifulSoup(text, 'html.parser')
        div_entry = soup.find_all('div', class_='itemContents')
        if len(div_entry) == 0:
            return 0
        for addon_entry in div_entry:
            addon_id = addon_entry.find('a').attrs.get('href').split('=')[1]
            title = addon_entry.find('div', {'class': 'workshopItemTitle'}).text

            self._results[addon_id] = title
        return len(div_entry)

