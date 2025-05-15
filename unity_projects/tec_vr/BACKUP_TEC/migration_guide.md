# AstraDigital Engine Migration Guide

## Overview
This document provides guidance on how to transition from your old repositories (Machine_Goddess_REPO and TEC_OFFICE_REPO) to the new AstraDigital Engine repository structure.

## Backed Up Files
We've created a backup of your crucial files in `C:\TEC_CODE\BACKUP_TEC`. This includes:

- **Brand Guidelines**: `docs/TEC_Brand_Guidelines.md`
- **Documentation**: Various `.md` files with guides & system documentation
- **Configuration Templates**: Safe versions without sensitive data
- **Agent Code**: For reference in implementing the new system

## Migration Steps

### 1. Set Up AstraDigital Engine Repository
```powershell
# Clone the repository
git clone https://github.com/TEC-The-ELidoras-Codex/astradigital-engine.git C:\TEC_CODE\astradigital-engine

# Navigate to the repository
cd C:\TEC_CODE\astradigital-engine
```

### 2. Copy Important Assets
```powershell
# Create docs directory if it doesn't exist
mkdir -p docs

# Copy brand guidelines
cp C:\TEC_CODE\BACKUP_TEC\docs\TEC_Brand_Guidelines.md docs\
```

### 3. Configure Environment
- Create proper `.env` file with your credentials (don't use the old one directly)
- Set up configuration based on templates

### 4. Test New Implementation
- Run any test scripts in the new repository
- Verify core functionality

### 5. Clean Up Old Repositories
Once you've confirmed the new repository works as expected:

```powershell
# Optional: Create a final backup as a ZIP file
Compress-Archive -Path C:\TEC_CODE\BACKUP_TEC -DestinationPath C:\TEC_CODE\tec_final_backup.zip

# Remove old redundant repositories
Remove-Item -Recurse -Force C:\TEC_CODE\vscodetec\Machine_Goddess_REPO
Remove-Item -Recurse -Force C:\TEC_CODE\TEC_OFFICE_REPO
```

## Repository Structure
Your new AstraDigital Engine should follow a clean, organized structure:

```
astradigital-engine/
├── config/               # Configuration files
│   └── env.example       # Template for .env (no real credentials)
├── docs/                 # Documentation
│   └── TEC_Brand_Guidelines.md
├── src/                  # Core source code
│   ├── agents/           # AI agent implementations
│   ├── api/              # API services
│   └── utils/            # Utility functions
├── tests/                # Test suite
├── .env                  # Environment variables (gitignored)
└── README.md             # Project documentation
```

## Contact
If you encounter any issues during migration, consult the documentation or reach out for assistance.
