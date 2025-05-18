#!/usr/bin/env python3

import os
import tomli
from typing import Dict
from steamscraper.constants import ARK_SURVIVAL_EVOLVED_APPID


class ScraperConfig:
    """Configuration class for Steam credentials and settings.
    Reads a TOML configuration file, provides access to values as properties,
    and validates that all mandatory fields are present.
    """

    def __init__(self, config_file: str = "steam-credentials.conf"):
        """Initialize the configuration from a TOML file.
        Args:
            config_file: Path to the TOML configuration file
        Raises:
            FileNotFoundError: If the configuration file does not exist
            ValueError: If any mandatory fields are missing
        """
        self._config_file = config_file
        self._config_data = self._read_config()
        self._validate_config()

    def _read_config(self) -> Dict:
        """Read the TOML configuration file.
        Returns:
            Dictionary containing the configuration values
        Raises:
            FileNotFoundError: If the configuration file does not exist
        """
        if not os.path.exists(self._config_file):
            raise FileNotFoundError(f"Configuration file not found: {self._config_file}")

        with open(self._config_file, "rb") as f:
            return tomli.load(f)

    def _validate_config(self) -> None:
        """Validate that all mandatory fields are present in the configuration.
        Raises:
            ValueError: If any mandatory fields are missing
        """
        mandatory_fields = ["steamlogin", "password", "username", "steamid"]
        missing_fields = []

        for field in mandatory_fields:
            if field not in self._config_data:
                missing_fields.append(field)

        if missing_fields:
            raise ValueError(f"Missing mandatory fields in configuration: {', '.join(missing_fields)}")

    @property
    def appid(self) -> str:
        """Get the Steam Workshop App ID."""
        return self._config_data.get("appid", ARK_SURVIVAL_EVOLVED_APPID)

    @property
    def steamlogin(self) -> str:
        """Get the Steam user ID."""
        return self._config_data["steamlogin"]

    @property
    def password(self) -> str:
        """Get the Steam password."""
        return self._config_data["password"]

    @property
    def username(self) -> str:
        """Get the Steam username."""
        return self._config_data["username"]

    @property
    def steamid(self) -> str:
        """Get the Steam ID."""
        return self._config_data["steamid"]
