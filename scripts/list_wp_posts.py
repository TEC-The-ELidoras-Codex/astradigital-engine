#!/usr/bin/env python3
"""
WordPress Posts Listing Script for The Elidoras Codex.
Lists the most recent posts from WordPress with their categories.
"""
import os
import sys
import json
import logging
import argparse
from typing import Dict, Any, List
from pathlib import Path
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("TEC.WPPostLister")

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config', '.env')
load_dotenv(env_path)

# Import the WordPress components
try:
    from src.agents.wp_poster import WordPressAgent
except ImportError as e:
    logger.critical(f"Failed to import required modules: {e}")
    print(f"Error: Failed to import required modules. Make sure all dependencies are installed.")
    print(f"Details: {e}")
    sys.exit(1)
    
def main():
    """Main function to list WordPress posts."""
    parser = argparse.ArgumentParser(description="List recent WordPress posts with categories")
    parser.add_argument("--count", type=int, default=5, help="Number of posts to list (default: 5)")
    parser.add_argument("--status", type=str, default="any", help="Post status to filter by (publish, draft, any)")
    args = parser.parse_args()
    
    try:
        # Initialize WordPress agent
        config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config')
        wp_agent = WordPressAgent(config_path=config_path)
        
        # Get posts
        posts = get_posts(wp_agent, args.count, args.status)
        
        if not posts:
            print("No posts found matching the criteria.")
            return 0
            
        # Display posts
        print(f"\n{'=' * 60}")
        print(f"{'ID':<6} | {'STATUS':<10} | {'CATEGORIES':<30} | {'TITLE'}")
        print(f"{'-' * 60}")
        
        for post in posts:
            # Get post details
            post_id = post.get("id", "N/A")
            title = post.get("title", {}).get("rendered", "No Title")
            status = post.get("status", "unknown")
            
            # Get category names
            category_ids = post.get("categories", [])
            category_names = []
            
            for cat_id in category_ids:
                # Find the category name from the dictionary
                for slug, id_val in wp_agent.categories.items():
                    if id_val == cat_id:
                        category_names.append(slug)
                        break
            
            category_str = ", ".join(category_names) if category_names else "None"
            
            # Print post info
            print(f"{post_id:<6} | {status:<10} | {category_str:<30} | {title}")
        
        print(f"{'=' * 60}\n")
        return 0
        
    except Exception as e:
        logger.critical(f"An error occurred: {e}")
        print(f"Error: {e}")
        return 1

def get_posts(wp_agent, count=5, status="any"):
    """
    Get posts from WordPress.
    
    Args:
        wp_agent: The WordPress agent
        count: Number of posts to retrieve
        status: Post status (publish, draft, any)
        
    Returns:
        List of posts
    """
    if not wp_agent.api_base_url:
        logger.error("Cannot get posts: API base URL not set")
        return []
        
    try:
        # Build the URL with parameters
        url = f"{wp_agent.api_base_url}/posts?per_page={count}"
        
        # Add status filter if not "any"
        if status and status.lower() != "any":
            url += f"&status={status}"
            
        # Make the request
        response = wp_agent._try_multiple_auth_methods("GET", url)
        
        if response and response.status_code == 200:
            posts = response.json()
            logger.info(f"Retrieved {len(posts)} posts")
            return posts
        else:
            status_code = response.status_code if response else "No response"
            logger.error(f"Failed to get posts: Status {status_code}")
            return []
                
    except Exception as e:
        logger.error(f"Error retrieving posts: {e}")
        return []

if __name__ == "__main__":
    sys.exit(main())
