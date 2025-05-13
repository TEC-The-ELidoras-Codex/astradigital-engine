"""
Pytest fixtures and configurations for The Elidoras Codex tests.
"""
import os
import pytest
import logging
from pathlib import Path
from dotenv import load_dotenv

# Add the project root to the path
project_root = Path(__file__).parent.parent
if str(project_root) not in os.sys.path:
    os.sys.path.insert(0, str(project_root))

@pytest.fixture(scope="session", autouse=True)
def setup_environment():
    """Set up test environment variables."""
    # Load environment variables
    env_path = Path(__file__).parent / '.env'
    if not env_path.exists():
        env_path = project_root / 'config' / '.env'
    
    if env_path.exists():
        load_dotenv(env_path)
        yield
    else:
        pytest.skip(f"Environment file not found at {env_path}")

@pytest.fixture(scope="session")
def wordpress_config():
    """Return WordPress configuration from environment variables."""
    config = {
        'wp_url': os.getenv('WP_SITE_URL'),
        'wp_username': os.getenv('WP_USERNAME'),
        'wp_password': os.getenv('WP_PASSWORD'),
    }
    
    # Skip tests if WordPress credentials are missing
    if not all(config.values()):
        pytest.skip("WordPress credentials not configured")
    
    return config

@pytest.fixture
def sample_post_data():
    """Return sample post data for testing."""
    return {
        "title": "Test Post from AstraDigital Engine",
        "content": "This is a test post created by the AstraDigital Engine testing framework.",
        "status": "draft", 
        "categories": ["Test"],
        "tags": ["test", "automation", "tec"]
    }
