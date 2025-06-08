"""
Pytest-based tests for WordPress integration.
"""
import os
import pytest
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("TEC.Test.WordPress")

# Try to import WordPress components
try:
    from src.wordpress import test_wordpress_connection as check_wordpress_connection
    from src.wordpress.wordpress_xmlrpc import WordPressXMLRPC
    from src.agents.wp_poster import WordPressAgent
except ImportError as e:
    logger.error(f"Failed to import WordPress modules: {e}")
    pytest.skip("WordPress modules not available", allow_module_level=True)

class TestWordPressConnection:
    """Test WordPress connection and basic functionality."""
    
    def test_connection(self, wordpress_config):
        """Test basic WordPress connection."""
        result = check_wordpress_connection()
        assert result["success"] is True
        assert "site_url" in result
    
    def test_xmlrpc_connection(self, wordpress_config):
        """Test WordPress XML-RPC connection."""
        wp = WordPressXMLRPC()
        assert wp.is_connected() is True
    
    def test_get_recent_posts(self, wordpress_config):
        """Test retrieving recent posts."""
        wp = WordPressXMLRPC()
        posts = wp.get_recent_posts(5)
        assert isinstance(posts, list)
        # Even if there are no posts, it should return an empty list, not fail
    
    @pytest.mark.parametrize("post_status", ["draft"])
    def test_create_post(self, wordpress_config, sample_post_data, post_status):
        """Test creating a post in WordPress."""
        config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'config', 'config.yaml')
        agent = WordPressAgent(config_path)
        
        sample_post_data["status"] = post_status
        
        result = agent.create_post(
            title=sample_post_data["title"],
            content=sample_post_data["content"],
            category=sample_post_data["categories"][0] if sample_post_data["categories"] else "uncategorized",
            tags=sample_post_data["tags"],
            status=post_status
        )
        
        assert result["success"] is True
        assert "id" in result
        assert isinstance(result["id"], int)
        
        # Clean up - delete the post
        wp = WordPressXMLRPC()
        wp.delete_post(result["id"])

# Skip all tests in this module if WordPress credentials are not configured
def pytest_configure(config):
    if not os.getenv('WP_SITE_URL') or not os.getenv('WP_USERNAME') or not os.getenv('WP_PASSWORD'):
        pytest.skip("WordPress credentials not configured", allow_module_level=True)

