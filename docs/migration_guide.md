"""
TEC Migration Guide

This document provides instructions for migrating from the legacy repositories 
(Machine_Goddess_REPO and TEC_OFFICE_REPO) to the new AstraDigital Engine repository.
"""

# AstraDigital Engine Migration Guide

## Overview

This document outlines the process for transitioning from the legacy repositories to the new AstraDigital Engine. The consolidation aims to eliminate redundancy, improve security, and streamline development.

## What Has Been Preserved

The following important assets have been preserved:

- **Brand Guidelines**: `docs/TEC_Brand_Guidelines.md`
- **Base Agent Framework**: A cleaner implementation of the core agent functionality
- **Configuration Templates**: Without sensitive information
- **WordPress Integration**: (To be implemented)

## What Has Been Removed

The following redundant or sensitive items have been removed:

- **Duplicate Code**: Multiple implementations of the same functionality
- **Sensitive Credentials**: API keys, passwords, and tokens
- **Legacy Test Scripts**: That served their purpose
- **Merge Conflicts**: From previous development efforts

## Repository Structure

The new repository follows a clean, modular structure:

```
astradigital-engine/
├── config/               # Configuration files
│   └── env.example       # Template for .env (no real credentials)
├── docs/                 # Documentation
│   └── TEC_Brand_Guidelines.md
├── src/                  # Core source code
│   ├── agents/           # AI agent implementations
│   │   └── base_agent.py # Base agent class
│   ├── api/              # API services
│   └── utils/            # Utility functions
├── tests/                # Test suite
├── .env                  # Environment variables (gitignored)
├── .gitignore            # Specifies files to ignore in Git
├── requirements.txt      # Python dependencies
├── setup.py              # Setup script
└── README.md             # Project documentation
```

## Migration Checklist

1. ✅ Repository structure created
2. ✅ Brand guidelines transferred
3. ✅ Configuration templates created
4. ✅ Base agent functionality implemented
5. 🔲 WordPress integration
6. 🔲 AI agent implementations
7. 🔲 Testing framework

## Next Steps

1. Implement the WordPress integration in the new framework
2. Add AI agent implementations (Airth, Budlee, Sassafras)
3. Create proper documentation for new implementations
4. Add tests for core functionality
5. Set up CI/CD pipeline

## References

Keep a backup of the old repositories until the migration is complete at:
`C:\TEC_CODE\BACKUP_TEC`
