# TEC Repository Organization

This document outlines the organization structure of the TEC_CODE repository.

## Directory Structure

The repository is organized as follows:

### Core Directories

- `/src` - Contains the main source code for the Astradigital Engine
- `/api` - API implementation files
- `/tests` - Formal test suite using pytest
- `/scripts` - Utility scripts for various operations
- `/docs` - Documentation files
- `/data` - Data files and storage
- `/config` - Configuration files

### Special Purpose Directories

- `/Instructions` - Contains instruction files for AI agents and systems
  - Stores all directive files that define capabilities, personalities, and constraints for AI agents
  - Example: `TEC_ECHO_ALPHA.instructions.md` for Budlee the anthrobunny bot

- `/scripts/Tests` - Contains legacy test scripts
  - Stores older test scripts that are kept for reference but aren't part of the formal test framework
  - These scripts may be useful for quick testing or debugging certain functionality
  - Examples include WordPress testing scripts, roadmap posting tests, etc.

## Testing Framework

The formal testing framework uses pytest and is organized in the `/tests` directory:

- `/tests/unit` - Unit tests for individual components
- `/tests/integration` - Integration tests for complex interactions
- `/tests/wordpress` - Specific tests for WordPress functionality

The legacy tests in `/scripts/Tests` are preserved for reference but should not be used as the primary testing method.

## Documentation

All components should be properly documented:
- Each directory should contain a README.md explaining its purpose
- Code files should include appropriate comments and docstrings
- The docs directory contains detailed information about specific features and systems
