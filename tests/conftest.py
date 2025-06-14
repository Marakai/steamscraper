import sys
import os
from unittest.mock import MagicMock

# Mock the steam module
steam_mock = MagicMock()
steam_mock.webauth = MagicMock()
sys.modules['steam'] = steam_mock
sys.modules['steam.webauth'] = steam_mock.webauth

# Mock the bs4 module
bs4_mock = MagicMock()
bs4_mock.BeautifulSoup = MagicMock()
sys.modules['bs4'] = bs4_mock

# Mock the tomli module
tomli_mock = MagicMock()
# Create a default config with all required fields
default_config = {
    "steamlogin": "test_steamlogin",
    "password": "test_password",
    "username": "test_username",
    "steamid": "test_steamid",
    "appid": "346110"
}
tomli_mock.load = MagicMock(return_value=default_config)
tomli_mock.loads = MagicMock(return_value=default_config)
sys.modules['tomli'] = tomli_mock

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
