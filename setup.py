"""
This file is kept for backwards compatibility with tools that don't support pyproject.toml.
All configuration is now in pyproject.toml.
"""

import setuptools

# Redirect to use pyproject.toml for configuration
setuptools.setup()
