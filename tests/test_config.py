import pytest
from unittest.mock import mock_open, patch
from steamscraper.config import ScraperConfig
from steamscraper.constants import ARK_SURVIVAL_EVOLVED_APPID


@pytest.fixture
def valid_toml_content():
    """Fixture providing valid TOML configuration content."""
    return f"""
    # Steam credentials configuration file
    appid = "{ARK_SURVIVAL_EVOLVED_APPID}"
    steamlogin = "test_steamlogin"
    password = "test_password"
    username = "test_username"
    steamid = "test_steamid"
    """.encode('utf-8')


@pytest.fixture
def invalid_toml_content():
    """Fixture providing invalid TOML configuration content (missing mandatory fields)."""
    return f"""
    # Steam credentials configuration file
    appid = "{ARK_SURVIVAL_EVOLVED_APPID}"
    # Missing mandatory fields
    """.encode('utf-8')


def test_init_with_valid_config(valid_toml_content):
    """Test initialization with a valid configuration file."""
    with patch("builtins.open", mock_open(read_data=valid_toml_content)):
        with patch("os.path.exists", return_value=True):
            config = ScraperConfig(config_file="test.conf")

            # Verify properties
            assert config.appid == ARK_SURVIVAL_EVOLVED_APPID
            assert config.steamlogin == "test_steamlogin"
            assert config.password == "test_password"
            assert config.username == "test_username"
            assert config.steamid == "test_steamid"


def test_init_with_nonexistent_file():
    """Test initialization with a nonexistent configuration file."""
    with patch("os.path.exists", return_value=False):
        with pytest.raises(FileNotFoundError) as excinfo:
            ScraperConfig(config_file="nonexistent.conf")

        assert "Configuration file not found" in str(excinfo.value)


def test_init_with_invalid_config(invalid_toml_content):
    """Test initialization with an invalid configuration file (missing mandatory fields)."""
    # Create an invalid config with only appid
    invalid_config = {"appid": ARK_SURVIVAL_EVOLVED_APPID}

    with patch("builtins.open", mock_open(read_data=invalid_toml_content)):
        with patch("os.path.exists", return_value=True):
            with patch("tomli.load", return_value=invalid_config):
                with pytest.raises(ValueError) as excinfo:
                    ScraperConfig(config_file="invalid.conf")

                # Verify error message contains missing fields
                assert "Missing mandatory fields" in str(excinfo.value)
                assert "steamlogin" in str(excinfo.value)
                assert "password" in str(excinfo.value)
                assert "username" in str(excinfo.value)
                assert "steamid" in str(excinfo.value)


def test_custom_appid(valid_toml_content):
    """Test custom appid value."""
    custom_toml = valid_toml_content.replace(
        f'appid = "{ARK_SURVIVAL_EVOLVED_APPID}"'.encode(), 
        b'appid = "123456"'
    )

    # Create a config with custom appid
    custom_config = {
        "appid": "123456",
        "steamlogin": "test_steamlogin",
        "password": "test_password",
        "username": "test_username",
        "steamid": "test_steamid"
    }

    with patch("builtins.open", mock_open(read_data=custom_toml)):
        with patch("os.path.exists", return_value=True):
            with patch("tomli.load", return_value=custom_config):
                config = ScraperConfig(config_file="test.conf")

                # Verify custom appid
                assert config.appid == "123456"


def test_default_appid(valid_toml_content):
    """Test default appid value when not specified in config."""
    custom_toml = valid_toml_content.replace(
        f'appid = "{ARK_SURVIVAL_EVOLVED_APPID}"'.encode(), 
        b''
    )

    # Create a config without appid
    default_config = {
        "steamlogin": "test_steamlogin",
        "password": "test_password",
        "username": "test_username",
        "steamid": "test_steamid"
    }

    with patch("builtins.open", mock_open(read_data=custom_toml)):
        with patch("os.path.exists", return_value=True):
            with patch("tomli.load", return_value=default_config):
                config = ScraperConfig(config_file="test.conf")

                # Verify default appid
                assert config.appid == ARK_SURVIVAL_EVOLVED_APPID
