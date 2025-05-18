# Makefile for steamscraper project

.PHONY: init wheel tests clean install

# Install all dependencies via Poetry
init:
	poetry install

# Create the wheel package (depends on init)
wheel: init
	poetry build --format wheel

# Run pytest unit tests (depends on init)
tests: init
	poetry run pytest || true

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
	pip install --user --force-reinstall dist/*.whl || pip install --force-reinstall dist/*.whl
