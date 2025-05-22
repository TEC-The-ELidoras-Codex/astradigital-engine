#!/usr/bin/env python3
"""
Direct WordPress posting script for debugging.
"""
import os
import sys
import argparse
from datetime import datetime

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import dotenv
from dotenv import load_dotenv

# Load environment variables from .env
config_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config')
env_path = os.path.join(config_dir, '.env')
load_dotenv(env_path)
print(f"Loaded environment from {env_path}")

# Import the WordPress agent
from src.agents.wp_poster import WordPressAgent

def main():
    # Create a simple test post
    title = f"Test Article - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    content = """
    <h2>This is a test article</h2>
    <p>Created to verify the WordPress posting functionality is working correctly.</p>
    <p>Generated at: {datetime}</p>
    """.format(datetime=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    print(f"Creating WordPress agent...")
    wp_agent = WordPressAgent(os.path.join('config'))
    print(f"WordPress agent created")
    
    # Try to get categories
    print(f"Fetching WordPress categories...")
    categories = wp_agent.get_categories(force_refresh=True)
    print(f"Categories: {categories}")
    
    # Create the post data
    post_data = {
        'title': title,
        'content': content,
        'status': 'draft'
    }
    
    # Post to WordPress
    print(f"Posting to WordPress: {title}")
    result = wp_agent.create_post(post_data, category="technology_ai")
    
    if result.get("success"):
        print(f"Success! Post created with ID: {result.get('id')}")
        print(f"URL: {result.get('link')}")
        return 0
    else:
        print(f"Failed to create post: {result.get('error_message')}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
