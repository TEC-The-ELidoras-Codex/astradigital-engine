"""
WordPress Test Script - Tests WordPress connectivity and configuration

Usage:
    python test_wordpress.py

This script will test your WordPress connectivity by checking credentials 
and attempting to create a draft post.
"""
import os
import sys
import logging
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("WordPress.Test")

# Load environment variables from the .env file
env_path = Path(__file__).parent.parent / "config" / ".env"
load_success = False

try:
    # Try to load env file
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
        load_success = True
    else:
        logger.warning(f".env file not found at {env_path}")
        # When running as main script, emit a more helpful message
        if __name__ == "__main__":
            print(f"\n⚠️ .env file not found. Please create {env_path} with your WordPress credentials.")
            print("You can use the .env.template file as a starting point.\n")
            sys.exit(1)
except Exception as e:
    logger.error(f"Error loading .env file: {e}")

# Validate environment variables
wp_url = os.getenv("WP_URL")
wp_username = os.getenv("WP_USERNAME")
wp_password = os.getenv("WP_PASSWORD")
if not all([wp_url, wp_username, wp_password]):
    logger.warning("WordPress credentials not fully configured in .env file.")
    config_error = True
else:
    config_error = False
    missing = []
    if not wp_url: missing.append("WP_URL")
    if not wp_username: missing.append("WP_USERNAME")
    if not wp_password: missing.append("WP_PASSWORD")
    print(f"\n❌ Missing environment variables: {', '.join(missing)}")
    print("Please update your .env file with the required credentials.\n")
    sys.exit(1)

# Import WordPress agent
try:
    from src.agents.wp_poster import WordPressAgent
except ImportError as e:
    logger.error(f"Failed to import WordPressAgent: {e}")
    print(f"\n❌ Failed to import WordPressAgent: {e}")
    sys.exit(1)

def test_wordpress_connection():
    """Test the WordPress connection and create a test draft post"""
    print("\n🔄 Testing WordPress connection...")
    try:
        wp_agent = WordPressAgent()
        
        # Test categories retrieval
        print("🔄 Testing category retrieval...")
        categories = wp_agent.get_categories()
        if categories:
            print(f"✅ Successfully retrieved {len(categories)} categories.")
            for category_id, category_name in categories.items():
                print(f"   - {category_name} (ID: {category_id})")
        else:
            print("⚠️ No categories returned, but connection might still be valid.")
            
        # Create test draft post
        print("\n🔄 Creating test draft post...")
        test_title = "Test Post from TEC Office Suite"
        test_content = """
        <p>This is a test post created by the TEC Office WordPress Test Script.</p>
        <p>If you see this post in your WordPress drafts, your WordPress integration is working correctly!</p>
        """
        
        post_data = {
            'title': test_title,
            'content': test_content,
            'status': 'draft',  # Always create as draft for testing
            'categories': [1],  # Default uncategorized
            'tags': ['test']
        }
        
        result = wp_agent.create_post(post_data)
        
        if result.get('success'):
            print(f"✅ Test post created successfully!")
            print(f"   Post ID: {result.get('post_id')}")
            print(f"   Title: {result.get('title')}")
            print(f"   Status: {result.get('status', 'draft')}")
            print("\n✅ WordPress integration is working correctly!")
            print("   You should see a test post in your WordPress drafts.")
        else:
            print(f"❌ Failed to create test post: {result.get('error', 'Unknown error')}")
    except Exception as e:
        logger.exception("WordPress test failed")
        print(f"❌ WordPress test failed: {str(e)}")
        return False
    
    return result.get('success', False)

if __name__ == "__main__":
    print("==== WordPress Integration Test ====")
    print(f"WordPress URL: {wp_url}")
    print(f"WordPress Username: {wp_username}")
    print(f"WordPress Password: {'*' * len(wp_password) if wp_password else 'NOT SET'}")
    
    success = test_wordpress_connection()
    
    if success:
        print("\n✅ All tests passed! Your WordPress integration is working correctly.")
        print("You can now use the Airth agent to post content to your WordPress site.")
    else:
        print("\n❌ Some tests failed. Please check the error messages and your configuration.")
