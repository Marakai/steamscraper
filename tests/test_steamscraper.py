import pytest
from unittest.mock import MagicMock, patch
from bs4 import BeautifulSoup
from steamscraper.steamapi import SteamScraper


@pytest.fixture
def mock_webauth():
    """Mock the steam.webauth module for testing."""
    with patch('steam.webauth.WebAuth') as mock_webauth:
        # Create a mock WebAuth instance
        mock_user = MagicMock()
        mock_user.username = "test_user"
        mock_user.session.get.return_value = MagicMock()
        mock_user.login.return_value = MagicMock()
        mock_user.cli_login.return_value = MagicMock()

        # Make the WebAuth constructor return our mock
        mock_webauth.return_value = mock_user

        yield mock_user


@pytest.fixture
def mock_bs4():
    """Mock BeautifulSoup for testing."""
    with patch('steamscraper.steamapi.workshop_client.BeautifulSoup') as mock_bs:
        yield mock_bs


class TestSteamScraper:
    """Test cases for the SteamScraper class."""

    def test_init_with_credentials(self, mock_webauth):
        """Test initialization with username and password."""
        scraper = SteamScraper(userid="test_user", pw="test_pass", mfa="12345")

        # Verify WebAuth was called with the correct username
        assert scraper._app_id == "346110"  # Default app ID
        mock_webauth.login.assert_called_once_with(password="test_pass", twofactor_code="12345")

    def test_init_with_prompt(self, mock_webauth):
        """Test initialization with prompt flag."""
        scraper = SteamScraper(userid="test_user", prompt=True)

        # Verify cli_login was called
        mock_webauth.cli_login.assert_called_once()

    def test_init_with_custom_appid(self, mock_webauth):
        """Test initialization with custom app ID."""
        scraper = SteamScraper(userid="test_user", pw="test_pass", appid="123456")

        # Verify app ID was set correctly
        assert scraper._app_id == "123456"

    def test_parse_userid(self, mock_webauth):
        """Test parse_userid method."""
        # Set up the mock response
        mock_response = MagicMock()
        mock_response.url = "https://steamcommunity.com/id/12345/myworkshopfiles/"
        mock_webauth.session.get.return_value = mock_response

        scraper = SteamScraper(userid="test_user", pw="test_pass")
        result = scraper._parse_userid()

        # Verify the correct URL was returned
        assert result == "https://steamcommunity.com/id/12345/myworkshopfiles/"
        # Verify the correct URL was requested
        mock_webauth.session.get.assert_called_with(
            f'https://steamcommunity.com/id/test_user/myworkshopfiles/?appid=346110&browsefilter=mysubscriptions&p=1&numberpage=30'
        )

    def test_parse_data_empty(self, mock_webauth, mock_bs4):
        """Test parse_data method with empty results."""
        # Set up the mock BeautifulSoup
        mock_soup = MagicMock()
        mock_soup.find_all.return_value = []
        mock_bs4.return_value = mock_soup

        scraper = SteamScraper(userid="test_user", pw="test_pass")
        result = scraper._parse_data(text="<html></html>")

        # Verify the correct result was returned
        assert result == 0
        # Verify BeautifulSoup was called with the correct arguments
        mock_bs4.assert_called_with("<html></html>", "html.parser")
        # Verify find_all was called with the correct arguments
        mock_soup.find_all.assert_called_with("div", class_="itemContents")

    def test_parse_data_with_results(self, mock_webauth, mock_bs4):
        """Test parse_data method with results."""
        # Set up the mock BeautifulSoup
        mock_soup = MagicMock()

        # Create mock div entries
        mock_div1 = MagicMock()
        mock_a1 = MagicMock()
        mock_a1.attrs = {"href": "?id=12345"}
        mock_div1.find.side_effect = [mock_a1, MagicMock(text="Test Mod 1")]

        mock_div2 = MagicMock()
        mock_a2 = MagicMock()
        mock_a2.attrs = {"href": "?id=67890"}
        mock_div2.find.side_effect = [mock_a2, MagicMock(text="Test Mod 2")]

        mock_soup.find_all.return_value = [mock_div1, mock_div2]
        mock_bs4.return_value = mock_soup

        scraper = SteamScraper(userid="test_user", pw="test_pass")
        result = scraper._parse_data(text="<html></html>")

        # Verify the correct result was returned
        assert result == 2
        # Verify the results were stored correctly
        assert scraper._results == {"12345": "Test Mod 1", "67890": "Test Mod 2"}

    def test_get_data(self, mock_webauth, monkeypatch):
        """Test get_data method."""
        # Mock the parse_userid and parse_data methods
        mock_parse_userid = MagicMock(return_value="https://steamcommunity.com/id/12345/myworkshopfiles/")
        mock_parse_data = MagicMock(side_effect=[2, 1, 0])  # Return 2, then 1, then 0 to simulate pagination

        # Create a response mock
        mock_response = MagicMock()
        mock_response.text = "<html></html>"
        mock_webauth.session.get.return_value = mock_response

        scraper = SteamScraper(userid="test_user", pw="test_pass")

        # Patch the methods
        monkeypatch.setattr(scraper, "parse_userid", mock_parse_userid)
        monkeypatch.setattr(scraper, "parse_data", mock_parse_data)

        # Set up the results
        scraper._results = {"12345": "Test Mod 1", "67890": "Test Mod 2", "54321": "Test Mod 3"}

        result = scraper.subscription_data()

        # Verify parse_userid was called
        mock_parse_userid.assert_called_once()

        # Verify parse_data was called 3 times (for 3 pages)
        assert mock_parse_data.call_count == 3

        # Verify the correct result was returned
        assert result == {"12345": "Test Mod 1", "67890": "Test Mod 2", "54321": "Test Mod 3"}

        # Verify session.get was called with the correct URLs
        expected_calls = [
            f'https://steamcommunity.com/id/12345/myworkshopfiles//?appid=346110&browsefilter=mysubscriptions&p=1&numberpage=30',
            f'https://steamcommunity.com/id/12345/myworkshopfiles//?appid=346110&browsefilter=mysubscriptions&p=2&numberpage=30',
            f'https://steamcommunity.com/id/12345/myworkshopfiles//?appid=346110&browsefilter=mysubscriptions&p=3&numberpage=30',
        ]

        for i, call in enumerate(mock_webauth.session.get.call_args_list):
            assert call[0][0] == expected_calls[i]
