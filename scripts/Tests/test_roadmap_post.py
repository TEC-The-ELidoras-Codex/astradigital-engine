"""
Test WordPress Roadmap Article Posting - Tests the ability to post roadmap articles via Airth

Usage:
    python test_roadmap_post.py [--publish]

This script will test Airth's ability to create and post a roadmap article to WordPress.
By default, the article is created as a draft. Use --publish to create a published post.
"""
import os
import sys
import logging
import argparse
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join("logs", "wp_posting_test.log"))
    ]
)
logger = logging.getLogger("WordPress.RoadmapTest")

# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

# Parse command line arguments
parser = argparse.ArgumentParser(description="Test WordPress roadmap article posting.")
parser.add_argument("--publish", action="store_true", help="Publish the article instead of saving as draft")
parser.add_argument("--debug", action="store_true", help="Enable debug logging")
args = parser.parse_args()

# Set log level
if args.debug:
    logger.setLevel(logging.DEBUG)
    logging.getLogger().setLevel(logging.DEBUG)

# Load environment variables from the .env file
env_path = Path(__file__).parent.parent / "config" / ".env"
if not env_path.exists():
    logger.error(f".env file not found at {env_path}. Please create this file with your credentials.")
    print(f"\n⚠️ .env file not found. Please create {env_path} with your credentials.")
    print("You can use the .env.template file as a starting point.\n")
    sys.exit(1)

load_dotenv(dotenv_path=env_path)

# Verify environment variables
required_vars = ["WP_URL", "WP_USERNAME", "WP_PASSWORD", "OPENAI_API_KEY"]
missing_vars = [var for var in required_vars if not os.getenv(var)]
if missing_vars:
    logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
    print(f"\n❌ Missing required environment variables: {', '.join(missing_vars)}")
    print("Please update your .env file with the required credentials.\n")
    sys.exit(1)

# Import Airth agent
try:
    from src.agents.airth_agent import AirthAgent
except ImportError as e:
    logger.error(f"Failed to import AirthAgent: {e}")
    print(f"\n❌ Failed to import AirthAgent: {e}")
    sys.exit(1)

def test_roadmap_posting():
    """Test Airth's ability to post a roadmap article to WordPress"""
    print("\n🔄 Initializing Airth agent...")
    
    try:
        # Initialize Airth agent
        airth = AirthAgent()
        print("✅ Airth agent initialized successfully.")
        
        # Get post status from arguments
        post_status = "publish" if args.publish else "draft"
        print(f"🔄 Will create article as: {post_status}")
        
        # Define a simple roadmap for testing
        test_roadmap = """
        The TEC AI Employee Suite: Test Roadmap
        
        Phase 1: Development Foundation
        - Complete Docker environment setup
        - Implement WordPress posting functionality
        - Fix security issues with API keys
        
        Phase 2: Enhanced Features
        - Add analytics capabilities
        - Implement multi-agent collaboration
        - Create advanced memory systems
        
        Phase 3: User Experience
        - Develop intuitive admin interfaces
        - Create user customization options
        - Deploy cross-platform support
        """
        
        print("\n🔄 Generating and posting roadmap article...")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        test_roadmap = f"Test Roadmap - {timestamp}\n\n{test_roadmap}"
        
        # Call Airth's method to create and post the article
        result = airth.create_wordpress_article_about_roadmap(test_roadmap, post_status)
        
        if result.get("success"):
            print("\n✅ Roadmap article posted successfully!")
            print(f"   Title: {result.get('title')}")
            if 'wp_response' in result and 'post_id' in result['wp_response']:
                print(f"   Post ID: {result['wp_response']['post_id']}")
            print(f"   Status: {post_status}")
            print(f"   Keywords: {', '.join(result.get('keywords', []))}")
            print("\n✅ Summary: Airth's WordPress posting functionality is working correctly!")
            
            # Print WordPress admin link
            wp_url = os.getenv("WP_URL", "").replace("/xmlrpc.php", "")
            if wp_url and 'wp_response' in result and 'post_id' in result['wp_response']:
                admin_url = f"{wp_url}/wp-admin/post.php?post={result['wp_response']['post_id']}&action=edit"
                print(f"\n📝 View/Edit in WordPress Admin: {admin_url}")
            
            if post_status == "publish":
                if wp_url and 'wp_response' in result and 'post_id' in result['wp_response']:
                    post_url = f"{wp_url}/?p={result['wp_response']['post_id']}"
                    print(f"🌐 View Published Post: {post_url}")
                else:
                    print("✅ Article published! Visit your WordPress site to view it.")
            else:
                print("✅ Article saved as draft. Log into WordPress admin to review and publish.")
                
            return True
        else:
            print(f"\n❌ Failed to post roadmap article: {result.get('error')}")
            if 'details' in result:
                print(f"   Details: {result.get('details')}")
            return False
    except Exception as e:
        logger.exception("Error during roadmap posting test")
        print(f"\n❌ Error during roadmap posting test: {str(e)}")
        return False

if __name__ == "__main__":
    print("==== WordPress Roadmap Article Posting Test ====")
    print(f"Mode: {'PUBLISH' if args.publish else 'DRAFT'}")
    print(f"Debug: {'Enabled' if args.debug else 'Disabled'}")
    
    success = test_roadmap_posting()
    
    if success:
        print("\n✅ Test completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Test failed. Please check the error messages.")
        sys.exit(1)
