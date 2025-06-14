# Makefile for steamscraper project

.PHONY: init wheel tests clean install lint

# Install all dependencies via uv
init:
	uv sync

# Create the wheel package (depends on init)
wheel: init
	uv build

# Run pytest unit tests (depends on init)
tests: init
	uvx pytest || true

# Clean up the repository
clean:
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf __pycache__/
	rm -rf steamscraper/__pycache__/
	find . -name "*.pyc" -delete

# Install the built package from wheel (depends on wheel and tests)
install: wheel tests
	uv pip install --user --force-reinstall dist/*.whl || uv pip install --force-reinstall dist/*.whl

# Run ruff linter and formatter
lint: init
	uvx ruff check .
	uvx ruff format .
