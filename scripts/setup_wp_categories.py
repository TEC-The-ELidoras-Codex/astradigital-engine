#!/usr/bin/env python3
"""
WordPress Category Setup Script for Airth News Automation.

This script creates the required categories in WordPress for the Airth News Automation system.
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
        logging.FileHandler(os.path.join(log_dir, "wp_category_setup.log"))
    ]
)
logger = logging.getLogger("WPCategorySetup")

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

def main():
    """
    Main function to set up WordPress categories.
    """
    logger.info("Starting WordPress category setup")
    
    # Required categories for Airth News Automation
    required_categories = [
        {"name": "AI Technology", "slug": "technology_ai"},
        {"name": "Technology News", "slug": "technology_news"},
        {"name": "Technology Analysis", "slug": "technology_analysis"},
        {"name": "Technology Trends", "slug": "technology_trends"},
        {"name": "Technology Business", "slug": "technology_business"},
        {"name": "Technology Research", "slug": "technology_research"},
        {"name": "Creative Explorations", "slug": "creative_explorations"}
    ]
    
    # Initialize WordPress agent
    try:
        config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config')
        wp_agent = WordPressAgent(config_path=config_path)
        logger.info("WordPress Agent initialized successfully")
        
        # Get existing categories
        existing_categories = wp_agent.get_categories()
        logger.info(f"Found {len(existing_categories)} existing categories")
        
        # Create missing categories
        success_count = 0
        for category in required_categories:
            name = category["name"]
            slug = category["slug"]
            
            # Check if category already exists
            if slug in wp_agent.categories and wp_agent.categories[slug]:
                logger.info(f"Category '{name}' (slug: {slug}) already exists with ID {wp_agent.categories[slug]}")
                success_count += 1
            else:
                # Create the category
                category_id = wp_agent.create_category(name, slug)
                if category_id:
                    logger.info(f"Created category '{name}' (slug: {slug}) with ID {category_id}")
                    success_count += 1
                else:
                    logger.error(f"Failed to create category '{name}' (slug: {slug})")
        
        # Output summary
        logger.info(f"Category setup completed. {success_count}/{len(required_categories)} categories created/verified.")
        
        if success_count == len(required_categories):
            print("\n✅ SUCCESS! All required WordPress categories have been created.")
            print("You can now use the Airth News Automation system with WordPress.")
        else:
            print(f"\n⚠️ WARNING: Only {success_count}/{len(required_categories)} categories were created/verified.")
            print("The Airth News Automation system may not work properly with WordPress.")
        
        return 0
        
    except Exception as e:
        logger.critical(f"Failed to set up WordPress categories: {e}")
        print(f"\n❌ ERROR: Failed to set up WordPress categories: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
