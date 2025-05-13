# The Elidoras Codex - AstraDigital Engine

## Project Structure

The AstraDigital Engine is organized into the following directories:

- `api/`: API endpoints and interfaces
- `assets/`: Static assets like images, fonts, etc.
- `builds/`: Build outputs for different platforms
- `config/`: Configuration files and settings
- `data/`: Data files, lore, and storage
- `docs/`: Documentation files
- `logs/`: Log files
- `scripts/`: Utility scripts for various operations
- `src/`: Source code for the engine
- `TEC_AI_ENGINE/`: Unity-based AI engine integration
- `tests/`: Test files and frameworks
- `theme/`: WordPress theme for The Elidoras Codex
- `unity_projects/`: Unity project files

## Getting Started

To set up the development environment:

1. Clone this repository
2. Copy `.env.example` to `.env` and fill in your credentials
   ```powershell
   # Windows
   .\scripts\setup_env.ps1
   
   # Linux/macOS
   ./scripts/setup_env.sh
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running Tests

Tests are organized by category:

- **Unit Tests**: Basic component testing
- **Integration Tests**: Testing component interactions
- **WordPress Tests**: WordPress integration testing

Run tests using the provided scripts:

```powershell
# Windows
.\run_tests.ps1 all         # Run all tests
.\run_tests.ps1 wordpress   # Run WordPress tests only
.\run_tests.ps1 integration # Run integration tests only
.\run_tests.ps1 unit        # Run unit tests only

# Add -v for verbose output
.\run_tests.ps1 all -v
```

```bash
# Linux/macOS
python run_tests.py all         # Run all tests
python run_tests.py wordpress   # Run WordPress tests only
python run_tests.py integration # Run integration tests only
python run_tests.py unit        # Run unit tests only

# Add --verbose for verbose output
python run_tests.py all --verbose
```

## Documentation

For detailed documentation on specific components:

- WordPress Integration: See `docs/wordpress_integration.md`
- Docker Deployment: See `docs/docker_deployment_guide.md`
- VR Development: See `docs/vr_development.md`
- AIRTH Timer: See `docs/timer_functionality.md`

## License

See the [LICENSE](LICENSE) file for license rights and limitations.
