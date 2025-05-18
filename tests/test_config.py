#!/usr/bin/env python3

import pytest
from unittest.mock import patch, mock_open
from steamscraper.config import SteamConfig
from steamscraper.constants import ARK_SURVIVAL_EVOLVED_APPID


@pytest.fixture
def mock_toml_file():
    """Mock a valid TOML configuration file."""
    toml_content = f"""
    # Steam credentials configuration file
    appid = "{ARK_SURVIVAL_EVOLVED_APPID}"
    steamlogin = "test_steamlogin"
    password = "test_password"
    username = "test_username"
    steamid = "test_steamid"
    """
    return toml_content.encode('utf-8')


@pytest.fixture
def mock_invalid_toml_file():
    """Mock an invalid TOML configuration file with missing fields."""
    toml_content = f"""
    # Steam credentials configuration file
    appid = "{ARK_SURVIVAL_EVOLVED_APPID}"
    steamlogin = "test_steamlogin"
    # Missing password, username, and steamid
    """
    return toml_content.encode('utf-8')


class TestSteamConfig:
    """Test cases for the SteamConfig class."""

    def test_init_with_valid_config(self, mock_toml_file):
        """Test initialization with a valid configuration file."""
        with patch("builtins.open", mock_open(read_data=mock_toml_file)):
            with patch("os.path.exists", return_value=True):
                config = SteamConfig(config_file="test.conf")

                # Verify properties
                assert config.appid == ARK_SURVIVAL_EVOLVED_APPID
                assert config.steamlogin == "test_steamlogin"
                assert config.password == "test_password"
                assert config.username == "test_username"
                assert config.steamid == "test_steamid"

    def test_init_with_nonexistent_file(self):
        """Test initialization with a nonexistent configuration file."""
        with patch("os.path.exists", return_value=False):
            with pytest.raises(FileNotFoundError):
                SteamConfig(config_file="nonexistent.conf")

    def test_init_with_invalid_config(self, mock_invalid_toml_file):
        """Test initialization with an invalid configuration file (missing mandatory fields)."""
        with patch("builtins.open", mock_open(read_data=mock_invalid_toml_file)):
            with patch("os.path.exists", return_value=True):
                with pytest.raises(ValueError) as excinfo:
                    SteamConfig(config_file="invalid.conf")

                # Verify error message contains missing fields
                assert "password" in str(excinfo.value)
                assert "username" in str(excinfo.value)
                assert "steamid" in str(excinfo.value)

    def test_custom_appid(self, mock_toml_file):
        """Test custom appid value."""
        custom_toml = mock_toml_file.replace(f'appid = "{ARK_SURVIVAL_EVOLVED_APPID}"'.encode(), b'appid = "123456"')

        with patch("builtins.open", mock_open(read_data=custom_toml)):
            with patch("os.path.exists", return_value=True):
                config = SteamConfig(config_file="test.conf")

                # Verify custom appid
                assert config.appid == "123456"

    def test_default_appid(self, mock_toml_file):
        """Test default appid value when not specified in config."""
        custom_toml = mock_toml_file.replace(f'appid = "{ARK_SURVIVAL_EVOLVED_APPID}"'.encode(), b'')

        with patch("builtins.open", mock_open(read_data=custom_toml)):
            with patch("os.path.exists", return_value=True):
                config = SteamConfig(config_file="test.conf")

                # Verify default appid
                assert config.appid == ARK_SURVIVAL_EVOLVED_APPID
