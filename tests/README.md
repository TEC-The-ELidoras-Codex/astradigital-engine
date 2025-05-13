# TEC Testing Framework

This directory contains all formal tests for The Elidoras Codex's AstraDigital Engine.

> **Note**: Legacy test scripts (older versions) have been moved to the `/scripts/Tests` directory and are kept for reference purposes only.

## Structure

- **`unit/`**: Contains unit tests for individual components and functions
- **`integration/`**: Contains tests for integrated components and external API connections
- **`wordpress/`**: Contains specific WordPress integration tests

## Running Tests

To run all tests:

```bash
python -m pytest tests/
```

To run a specific test category:

```bash
python -m pytest tests/wordpress/
python -m pytest tests/integration/
python -m pytest tests/unit/
```

## Adding New Tests

When adding new tests:

1. Place them in the appropriate directory based on test type
2. Follow the naming convention: `test_*.py`
3. Add proper docstrings explaining what the test covers
4. Try to include both positive and negative test cases

## Test Dependencies

Some tests may require environment variables or credentials to be set up. Check the documentation for each test module for specific requirements.
