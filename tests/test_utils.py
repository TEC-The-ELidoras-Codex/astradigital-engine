"""
Test utilities for The Elidoras Codex AstraDigital Engine.
"""
import os
import sys
import json
import logging
from pathlib import Path
from dotenv import load_dotenv

# Add parent directory to path to allow imports from src
sys.path.insert(0, str(Path(__file__).parent.parent))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('tec.test')

def load_test_env():
    """Load environment variables from .env file."""
    # Try to load from tests/.env first, then fall back to config/.env
    env_path = Path(__file__).parent / '.env'
    if not env_path.exists():
        env_path = Path(__file__).parent.parent / 'config' / '.env'
    
    load_dotenv(env_path)
    logger.info(f"Loaded environment from {env_path}")
    
    # Check for required variables
    required_vars = ['WP_SITE_URL', 'WP_USERNAME']
    missing = [var for var in required_vars if not os.getenv(var)]
    
    if missing:
        logger.warning(f"Missing required environment variables: {', '.join(missing)}")
        return False
    return True

def load_test_data(filename):
    """Load test data from a JSON file in the tests/data directory."""
    data_path = Path(__file__).parent / 'data' / filename
    try:
        with open(data_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"Test data file not found: {data_path}")
        return {}
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON in test data file: {data_path}")
        return {}

def get_test_config():
    """Get test configuration."""
    return {
        'wp_url': os.getenv('WP_SITE_URL'),
        'wp_username': os.getenv('WP_USERNAME'),
        'wp_password': os.getenv('WP_PASSWORD'),
        'debug': os.getenv('DEBUG_MODE', 'false').lower() == 'true'
    }
