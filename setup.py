"""
AstraDigital Engine - Setup Script
"""
import os
import shutil
import sys
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("astradigital-setup")

def setup_environment():
    """Set up the AstraDigital Engine environment."""
    logger.info("Setting up AstraDigital Engine environment...")
    
    # Check for .env file
    env_example = Path("config/env.example")
    env_file = Path("config/.env")
    
    if not env_example.exists():
        logger.error("Missing env.example file. Setup cannot continue.")
        return False
    
    if not env_file.exists():
        logger.warning("No .env file found. Creating one from template...")
        shutil.copy(env_example, env_file)
        logger.info("Created .env file. Please edit it with your credentials.")
    
    # Create required directories
    directories = [
        "logs",
        "data",
        "data/memories",
        "data/storage"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        logger.info(f"Created directory: {directory}")
    
    # Initialize empty files
    Path("logs/.gitkeep").touch()
    
    logger.info("Environment setup complete.")
    logger.info("-" * 50)
    logger.info("Next steps:")
    logger.info("1. Edit config/.env with your credentials")
    logger.info("2. Run 'python -m src.main' to start the engine")
    logger.info("-" * 50)
    
    return True

if __name__ == "__main__":
    if setup_environment():
        logger.info("Setup completed successfully!")
    else:
        logger.error("Setup failed. Please check the errors above.")
