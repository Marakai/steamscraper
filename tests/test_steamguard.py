#!/usr/bin/env python3

import pytest
from unittest.mock import patch, MagicMock

from steamscraper.steamapi import get_steamguard_code


class TestSteamGuard:
    """Test cases for the steamguard module."""

    @patch('subprocess.run')
    def test_get_steamguard_code_success(self, mock_run):
        """Test get_steamguard_code with successful execution."""
        # Set up the mock to return a successful result
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "123456\n"
        mock_result.stderr = ""
        mock_run.return_value = mock_result

        # Call the function
        result = get_steamguard_code()

        # Verify the result
        assert result == "123456"

        # Verify subprocess.run was called with the correct arguments
        mock_run.assert_called_once_with(
            ["/usr/local/bin/steamguard", "-v", "warn", "code"],
            capture_output=True,
            text=True,
            check=False
        )

    @patch('subprocess.run')
    def test_get_steamguard_code_error(self, mock_run):
        """Test get_steamguard_code with error execution."""
        # Set up the mock to return a failed result
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stderr = "Error: Invalid command"
        mock_run.return_value = mock_result

        # Call the function and expect an exception
        with pytest.raises(RuntimeError) as excinfo:
            get_steamguard_code()

        # Verify the exception details
        assert "Failed to get Steam Guard code: Error: Invalid command" in str(excinfo.value)

    @patch('subprocess.run')
    def test_get_steamguard_code_file_not_found(self, mock_run):
        """Test get_steamguard_code with FileNotFoundError."""
        # Set up the mock to raise a FileNotFoundError
        mock_run.side_effect = FileNotFoundError("No such file or directory: '/usr/local/bin/steamguard'")

        # Call the function and expect an exception
        with pytest.raises(FileNotFoundError):
            get_steamguard_code()
