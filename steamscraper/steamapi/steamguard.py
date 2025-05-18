#!/usr/bin/env python3

import subprocess


def get_steamguard_code() -> str:
    """Execute the steamguard CLI command to get a code.
    Runs "/usr/local/bin/steamguard -v warn code" and returns stdout output.
    Returns:
        str: The output from the steamguard command
    Raises:
        RuntimeError: If the command returns a non-zero exit code
        FileNotFoundError: If the steamguard executable is not found
    """
    # Run the command and capture stdout and stderr
    result = subprocess.run(
        ["/usr/local/bin/steamguard", "-v", "warn", "code"],
        capture_output=True,
        text=True,
        check=False  # Don't raise CalledProcessError
    )

    # Check if the command was successful
    if result.returncode != 0:
        error_message = result.stderr.strip() if result.stderr else f"Command failed with return code {result.returncode}"
        raise RuntimeError(f"Failed to get Steam Guard code: {error_message}")

    # Return the stdout output as a string
    return result.stdout.strip()
