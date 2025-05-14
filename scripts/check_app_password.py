#!/usr/bin/env python3
"""
Simple script to check if a WordPress application password is valid
by testing authentication against the WordPress REST API.
"""
import os
import sys
import requests
import argparse
import base64
from dotenv import load_dotenv
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("TEC.WPPasswordCheck")

# Find and load the .env file
script_dir = Path(__file__).parent
proj_root = script_dir.parent
env_path = proj_root / "config" / ".env"

if env_path.exists():
    load_dotenv(env_path)
    logger.info(f"Loaded environment from {env_path}")
else:
    logger.error(f"Could not find .env file at {env_path}")
    sys.exit(1)

def check_app_password(wp_url=None, wp_username=None, wp_password=None):
    """Test WordPress application password with REST API."""
    # Use provided values or fall back to env vars
    wp_url = wp_url or os.getenv("WP_URL")
    wp_username = wp_username or os.getenv("WP_USERNAME")
    wp_password = wp_password or os.getenv("WP_PASSWORD")
    
    if not all([wp_url, wp_username, wp_password]):
        logger.error("Missing required WordPress credentials")
        return False
        
    # Make sure URL doesn't end with a slash
    wp_url = wp_url.rstrip('/')
    
    # REST API endpoint
    api_url = f"{wp_url}/wp-json/wp/v2/users/me"
    
    # Try application password with spaces
    auth_string = f"{wp_username}:{wp_password}"
    auth_encoded = base64.b64encode(auth_string.encode()).decode()
    
    headers = {
        'Authorization': f'Basic {auth_encoded}',
        'Content-Type': 'application/json'
    }
    
    try:
        logger.info(f"Testing application password against {api_url}")
        response = requests.get(api_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            user_data = response.json()
            logger.info(f"✅ Authentication successful! Logged in as: {user_data.get('name', 'Unknown')}")
            logger.info(f"User role(s): {', '.join(user_data.get('roles', ['unknown']))}")
            return True
        else:
            logger.error(f"❌ Authentication failed with status {response.status_code}")
            logger.error(f"Response: {response.text}")
            return False
    except Exception as e:
        logger.error(f"❌ Connection error: {str(e)}")
        return False

def main():
    """Main function with argument parsing."""
    parser = argparse.ArgumentParser(description="Check WordPress application password")
    parser.add_argument("--url", help="WordPress site URL")
    parser.add_argument("--user", help="WordPress username")
    parser.add_argument("--password", help="WordPress application password")
    parser.add_argument("--generate-instructions", action="store_true", 
                       help="Show instructions for generating a new application password")
    
    args = parser.parse_args()
    
    if args.generate_instructions:
        print("=" * 80)
        print("HOW TO GENERATE A WORDPRESS APPLICATION PASSWORD")
        print("=" * 80)
        print("1. Log in to your WordPress admin panel")
        print("2. Go to Users → Profile (or Users → Your Profile)")
        print("3. Scroll down to the 'Application Passwords' section")
        print("4. Enter a name for the application (e.g., 'Airth News Automation')")
        print("5. Click 'Add New Application Password'")
        print("6. Copy the generated password (it will look like: xxxx xxxx xxxx xxxx xxxx xxxx)")
        print("7. Update your .env file with this new password")
        print("8. Keep the spaces in the password when adding it to your .env file")
        print("=" * 80)
        print("NOTE: If you don't see the Application Passwords section,")
        print("      your site may not be using HTTPS or the feature might be disabled.")
        print("=" * 80)
        return
    
    # Run the check with provided args or env values
    check_app_password(args.url, args.user, args.password)

if __name__ == "__main__":
    main()
