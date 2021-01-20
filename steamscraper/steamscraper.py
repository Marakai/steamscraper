#!/usr/bin/env python3

from bs4 import BeautifulSoup
import steam.webauth as wa


class SteamScraper:
    def __init__(self, *, username: str, pw: str = '', mfa: str = '', prompt: bool = False):
        self._user = wa.WebAuth(username)
        if prompt:
            self._session = self._user.cli_login()
        else:
            self._session = self._user.login(password=pw, twofactor_code=mfa)
        self._results = {}

    def get_data(self):
        arksurvival_app_id = '346110'
        page = 1
        while True:
            # regardless of numberpage setting, always seem to get 10 at a time through API
            base_url = f'https://steamcommunity.com/id/marakai666/myworkshopfiles/?appid={arksurvival_app_id}&browsefilter=mysubscriptions&p={str(page)}&numberpage=30'
            rawdata = self._user.session.get(base_url)
            rawtext = rawdata.text
            counter = self.parse_data(text=rawtext)
            if counter == 0:
                break
            page += 1
        return self._results

    def parse_data(self, *, text: str) -> int:
        soup = BeautifulSoup(text, 'html.parser')
        div_entry = soup.find_all('div', class_='itemContents')
        if len(div_entry) == 0:
            return 0
        for addon_entry in div_entry:
            addon_id = addon_entry.find('a').attrs.get('href').split('=')[1]
            title = addon_entry.find('div', {'class': 'workshopItemTitle'}).text

            self._results[addon_id] = title
        return len(div_entry)

