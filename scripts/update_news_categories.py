#!/usr/bin/env python3
"""
WordPress Category Fix Script for Airth News Automation.

This script updates the news automation script to use the proper category IDs.
"""
import os
import sys
import logging
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure logging
log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs')
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join(log_dir, "airth_news_category_update.log"))
    ]
)
logger = logging.getLogger("AirthNewsCategoryUpdate")

# Import required modules
try:
    from dotenv import load_dotenv
    from src.agents.wp_poster import WordPressAgent
except ImportError as e:
    logger.critical(f"Failed to import required modules: {e}")
    print(f"Error: Failed to import required modules. Make sure all dependencies are installed.")
    print(f"Details: {e}")
    sys.exit(1)

# Load environment variables
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config', '.env')
load_dotenv(env_path)

def update_news_posts(days=7):
    """
    Update existing news posts to set the correct categories.
    
    Args:
        days: Number of days back to look for posts to update
    """
    logger.info(f"Starting WordPress category update for posts from the last {days} days")
    
    # Initialize WordPress agent
    try:
        config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config')
        wp_agent = WordPressAgent(config_path=config_path)
        logger.info("WordPress Agent initialized successfully")
        
        # Get recent posts
        posts = get_posts(wp_agent, status="draft")
        logger.info(f"Found {len(posts)} draft posts to check")
        
        # Filter for Airth News posts
        news_posts = [
            p for p in posts 
            if "google" in p.get("title", {}).get("rendered", "").lower() or 
               "guide" in p.get("title", {}).get("rendered", "").lower() or
               "technology" in p.get("title", {}).get("rendered", "").lower() or
               "ai" in p.get("title", {}).get("rendered", "").lower()
        ]
        
        logger.info(f"Found {len(news_posts)} AI/tech related posts to update")
        
        # Update each post
        updated_count = 0
        for post in news_posts:
            post_id = post.get("id")
            title = post.get("title", {}).get("rendered", "No Title")
            
            # Skip if already has a category
            if post.get("categories") and len(post.get("categories")) > 0:
                logger.info(f"Post {post_id} ({title}) already has categories, skipping")
                continue
                
            logger.info(f"Updating post {post_id}: {title}")
            
            # Assign appropriate category
            category = "technology_ai"  # Default
            
            # Check title for better category matches
            title_lower = title.lower()
            if "business" in title_lower or "startup" in title_lower:
                category = "technology_business"
            elif "research" in title_lower or "study" in title_lower:
                category = "technology_research"
            elif "trend" in title_lower or "future" in title_lower:
                category = "technology_trends"
            elif "analysis" in title_lower or "review" in title_lower:
                category = "technology_analysis"
            elif "creative" in title_lower or "art" in title_lower:
                category = "creative_explorations"
            elif "news" in title_lower or "latest" in title_lower:
                category = "technology_news"
                
            # Get category ID
            category_id = wp_agent.categories.get(category)
            
            if not category_id:
                logger.warning(f"Category '{category}' not found, using fallback")
                category_id = wp_agent.categories.get("technology_ai")
                
            if not category_id:
                logger.error(f"Failed to find category ID for '{category}'")
                continue
                
            # Update the post
            result = update_post_category(wp_agent, post_id, category_id)
            
            if result:
                logger.info(f"Successfully updated post {post_id} with category '{category}'")
                updated_count += 1
            else:
                logger.error(f"Failed to update post {post_id}")
                
        # Output summary
        logger.info(f"Category update completed. {updated_count}/{len(news_posts)} posts updated.")
        
        if updated_count > 0:
            print(f"\n✅ SUCCESS! Updated {updated_count} posts with appropriate categories.")
        else:
            print("\n⚠️ No posts were updated. See log for details.")
        
        return 0
        
    except Exception as e:
        logger.critical(f"Failed to update post categories: {e}")
        print(f"\n❌ ERROR: Failed to update post categories: {e}")
        return 1

def get_posts(wp_agent, status="any"):
    """Get posts from WordPress."""
    if not wp_agent.api_base_url:
        logger.error("Cannot get posts: API base URL not set")
        return []
        
    try:
        # Build the URL with parameters
        url = f"{wp_agent.api_base_url}/posts?per_page=20"
        
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

def update_post_category(wp_agent, post_id, category_id):
    """Update a post's category."""
    if not wp_agent.api_base_url:
        logger.error("Cannot update post: API base URL not set")
        return False
        
    try:
        # Build the URL
        url = f"{wp_agent.api_base_url}/posts/{post_id}"
        
        # Prepare the data
        data = {
            "categories": [category_id]
        }
        
        # Make the request
        response = wp_agent._try_multiple_auth_methods("POST", url, data)
        
        if response and response.status_code in [200, 201]:
            logger.info(f"Successfully updated post {post_id}")
            return True
        else:
            status_code = response.status_code if response else "No response"
            logger.error(f"Failed to update post {post_id}: Status {status_code}")
            return False
                
    except Exception as e:
        logger.error(f"Error updating post {post_id}: {e}")
        return False

if __name__ == "__main__":
    sys.exit(update_news_posts())
