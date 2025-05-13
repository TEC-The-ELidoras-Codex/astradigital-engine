#!/usr/bin/env python3
"""
Script to launch the TEC Office Hugging Face Space.
This script is designed to run both locally and in HF Spaces environment.
"""
import os
import sys
import argparse
import logging
from pathlib import Path
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("TEC.HFSpace")

# Directory setup
BASE_DIR = Path(__file__).resolve().parent
CONFIG_DIR = BASE_DIR / "config"
LOGS_DIR = BASE_DIR / "logs"

# Create necessary directories
os.makedirs(LOGS_DIR, exist_ok=True)
os.makedirs(CONFIG_DIR, exist_ok=True)

# Add the current directory to the path
sys.path.append(str(BASE_DIR))

# Check if we're running in a Hugging Face Space
HF_SPACE = os.environ.get('SPACE_ID') is not None
if HF_SPACE:
    logger.info("Running in Hugging Face Space environment")
    # In HF Space, load environment variables from the Secrets
    # which are automatically mapped to environment variables
else:
    logger.info("Running in local environment")
    # In local environment, load from .env file
    env_path = CONFIG_DIR / ".env"
    if env_path.exists():
        load_dotenv(env_path)
        logger.info(f"Loaded environment variables from {env_path}")
    else:
        logger.warning(f".env file not found at {env_path}")

# Check required environment variables
def check_env_vars():
    """Check if required environment variables are set."""
    required_vars = [
        'WP_URL', 
        'WP_USERNAME', 
        'WP_PASSWORD',
        'OPENAI_API_KEY'
    ]
    
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    
    if missing_vars:
        logger.warning(f"Missing environment variables: {', '.join(missing_vars)}")
        logger.warning("Some functionality may be limited")
    else:
        logger.info("All required environment variables are set")

# Import the Gradio app
try:
    from app import demo
    logger.info("Successfully imported Gradio app")
except ImportError as e:
    logger.error(f"Failed to import Gradio app: {e}")
    sys.exit(1)

def main():
    """Launch the Hugging Face Space app."""
    parser = argparse.ArgumentParser(description='Launch the TEC Office Hugging Face Space')
    parser.add_argument('--share', action='store_true', help='Create a public link')
    parser.add_argument('--port', type=int, default=7860, help='Port to run the app on')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    args = parser.parse_args()
    
    # Check environment variables
    check_env_vars()
    
    # Set server options
    if HF_SPACE:
        # In HF Space, use default settings
        server_name = "0.0.0.0"
        server_port = 7860
        share = False
        logger.info(f"Launching app in Hugging Face Space mode on port {server_port}")
    else:
        # Local development settings
        server_name = "0.0.0.0"
        server_port = args.port
        share = args.share
        logger.info(f"Launching app in local mode on port {server_port}")
        if share:
            logger.info("Creating a public link for sharing")
      # Set log level
    if args.debug:
        logger.setLevel(logging.DEBUG)
        logger.debug("Debug mode enabled")
    
    try:
        # Launch the app
        demo.launch(
            server_name=server_name, 
            server_port=server_port, 
            share=share,
            debug=args.debug,
            show_error=True
        )
        return 0
    except Exception as e:
        logger.error(f"Error launching app: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
