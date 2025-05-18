import pytest
from unittest.mock import MagicMock, patch
from steamscraper.steamapi.scraper import Scraper
from steamscraper.config import ScraperConfig
from steamscraper.constants import ARK_SURVIVAL_EVOLVED_APPID


@pytest.fixture
def mock_config():
    """Mock ScraperConfig for testing."""
    config = MagicMock(spec=ScraperConfig)
    config.appid = ARK_SURVIVAL_EVOLVED_APPID
    config.steamlogin = "test_steamlogin"
    config.password = "test_password"
    config.username = "test_username"
    config.steamid = "test_steamid"
    return config


@pytest.fixture
def mock_webauth():
    """Mock the steam.webauth module for testing."""
    with patch('steam.webauth.WebAuth') as mock_webauth_class:
        # Create a mock WebAuth instance
        mock_user = MagicMock()
        mock_session = MagicMock()
        mock_user.login.return_value = mock_session

        # Make the WebAuth constructor return our mock
        mock_webauth_class.return_value = mock_user

        yield mock_webauth_class, mock_user


@pytest.fixture
def mock_steamguard():
    """Mock the get_steamguard_code function for testing."""
    with patch('steamscraper.steamapi.scraper.get_steamguard_code') as mock_get_code:
        mock_get_code.return_value = "123456"
        yield mock_get_code


@pytest.fixture
def mock_bs4():
    """Mock BeautifulSoup for testing."""
    with patch('steamscraper.steamapi.scraper.BeautifulSoup') as mock_bs:
        yield mock_bs


def test_init(mock_config, mock_webauth, mock_steamguard):
    """Test initialization with configuration."""
    mock_webauth_class, mock_user = mock_webauth
    scraper = Scraper(config=mock_config)

    # Verify WebAuth was called with the correct username
    mock_webauth_class.assert_called_once_with(mock_config.steamlogin)

    # Verify steam_id_base was set correctly
    assert mock_user.steam_id_base == mock_config.steamid

    # Verify login was called with the correct password and twofactor_code
    mock_user.login.assert_called_once_with(
        password=mock_config.password, 
        twofactor_code="123456"
    )

    # Verify config was stored
    assert scraper._config == mock_config


def test_subscription_data(mock_config, mock_webauth, mock_steamguard, mock_bs4):
    """Test subscription_data method."""
    mock_webauth_class, mock_user = mock_webauth

    # Set up mock responses
    mock_response1 = MagicMock()
    mock_response1.text = "<html>response1</html>"

    mock_response2 = MagicMock()
    mock_response2.text = "<html>response2</html>"

    mock_response3 = MagicMock()
    mock_response3.text = "<html>response3</html>"

    mock_response4 = MagicMock()
    mock_response4.text = "<html>response4</html>"

    # Set up session.get to return our mock responses
    mock_user.login.return_value.get.side_effect = [
        mock_response1,  # First call for steamid, page 1
        mock_response2,  # Second call for steamid, page 2
        mock_response3,  # Third call for steamid, page 3
        mock_response4,  # First call for username, page 1
    ]

    # Create the scraper
    scraper = Scraper(config=mock_config)

    # Mock _parse_data to control the loop
    scraper._parse_data = MagicMock(side_effect=[2, 1, 0, 0])

    # Set up expected results
    scraper._results = {"12345": "Test Mod 1", "67890": "Test Mod 2"}

    # Call the method
    result = scraper.subscription_data()

    # Verify the correct URLs were requested
    expected_urls = [
        f'https://steamcommunity.com/id/{mock_config.steamid}/myworkshopfiles/?appid={mock_config.appid}&browsefilter=mysubscriptions&p=1',
        f'https://steamcommunity.com/id/{mock_config.steamid}/myworkshopfiles/?appid={mock_config.appid}&browsefilter=mysubscriptions&p=2',
        f'https://steamcommunity.com/id/{mock_config.steamid}/myworkshopfiles/?appid={mock_config.appid}&browsefilter=mysubscriptions&p=3',
        f'https://steamcommunity.com/id/{mock_config.username}/myworkshopfiles/?appid={mock_config.appid}&browsefilter=mysubscriptions&p=1',
    ]

    assert mock_user.login.return_value.get.call_count == 4
    for i, call in enumerate(mock_user.login.return_value.get.call_args_list):
        assert call[0][0] == expected_urls[i]

    # Verify _parse_data was called with the correct arguments
    assert scraper._parse_data.call_count == 4
    scraper._parse_data.assert_any_call(text="<html>response1</html>")
    scraper._parse_data.assert_any_call(text="<html>response2</html>")
    scraper._parse_data.assert_any_call(text="<html>response3</html>")
    scraper._parse_data.assert_any_call(text="<html>response4</html>")

    # Verify the correct result was returned
    assert result == {"12345": "Test Mod 1", "67890": "Test Mod 2"}


def test_parse_data_empty(mock_config, mock_webauth, mock_steamguard, mock_bs4):
    """Test _parse_data method with empty results."""
    mock_webauth_class, mock_user = mock_webauth

    # Set up mock BeautifulSoup
    mock_soup = MagicMock()
    mock_soup.find_all.return_value = []
    mock_bs4.return_value = mock_soup

    # Create the scraper
    scraper = Scraper(config=mock_config)

    # Call the method
    result = scraper._parse_data(text="<html></html>")

    # Verify BeautifulSoup was called with the correct arguments
    mock_bs4.assert_called_with("<html></html>", "html.parser")

    # Verify find_all was called with the correct arguments
    mock_soup.find_all.assert_called_with("div", class_="itemContents")

    # Verify the correct result was returned
    assert result == 0


def test_parse_data_with_results(mock_config, mock_webauth, mock_steamguard, mock_bs4):
    """Test _parse_data method with results."""
    mock_webauth_class, mock_user = mock_webauth

    # Set up mock BeautifulSoup
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

    # Create the scraper
    scraper = Scraper(config=mock_config)

    # Call the method
    result = scraper._parse_data(text="<html></html>")

    # Verify BeautifulSoup was called with the correct arguments
    mock_bs4.assert_called_with("<html></html>", "html.parser")

    # Verify find_all was called with the correct arguments
    mock_soup.find_all.assert_called_with("div", class_="itemContents")

    # Verify the correct result was returned
    assert result == 2

    # Verify the results were stored correctly
    assert scraper._results == {"12345": "Test Mod 1", "67890": "Test Mod 2"}
