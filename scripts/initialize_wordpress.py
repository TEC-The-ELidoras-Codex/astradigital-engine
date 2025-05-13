#!/usr/bin/env python3
"""
WordPress Initialization Script for TEC_OFFICE_REPO.
This script sets up initial WordPress categories, tags, and other content.
"""
import os
import sys
import logging
import argparse
import json
from typing import Dict, Any, List, Optional
from pathlib import Path
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("TEC.WordPressInit")

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables
load_dotenv(os.path.join('config', '.env'))

# Import the WordPress components
try:
    from src.agents.wp_poster import WordPressAgent
    from src.wordpress.wordpress_xmlrpc import WordPressXMLRPC
    WORDPRESS_MODULES_LOADED = True
except ImportError as e:
    logger.error(f"Failed to import WordPress modules: {e}")
    WORDPRESS_MODULES_LOADED = False

# TEC standard categories
TEC_CATEGORIES = [
    {
        "name": "Airth's Codex",
        "slug": "airths-codex",
        "description": "Deep insights and analysis from Airth, the AI Oracle of TEC."
    },
    {
        "name": "Technology & AI",
        "slug": "technology-ai",
        "description": "Explorations of technology, artificial intelligence, and their implications."
    },
    {
        "name": "Creative Explorations",
        "slug": "creative-explorations",
        "description": "Creative content, stories, and artistic expressions from Sassafras."
    },
    {
        "name": "Workflows & Automation",
        "slug": "workflows-automation",
        "description": "Productivity tips, workflows, and automation from Budlee."
    },
    {
        "name": "TEC Updates",
        "slug": "tec-updates",
        "description": "Updates about The Elidoras Codex project and AI agents."
    }
]

# TEC standard tags
TEC_TAGS = [
    "ai-writing",
    "ai-art",
    "ai-tools",
    "ai-ethics",
    "automation",
    "creativity",
    "productivity",
    "future-tech",
    "ai-collaboration",
    "digital-creativity",
    "tec-agents",
    "airth",
    "budlee",
    "sassafras"
]

def create_categories(wp_agent: WordPressAgent) -> Dict[str, Any]:
    """Create standard TEC categories in WordPress."""
    logger.info("Creating standard TEC categories...")
    
    results = {
        "success": True,
        "created": [],
        "existing": [],
        "failed": []
    }
    
    # Get existing categories
    existing_categories = wp_agent.get_categories()
    existing_slugs = [cat.get("slug", "") for cat in existing_categories]
    
    for category in TEC_CATEGORIES:
        cat_name = category["name"]
        cat_slug = category["slug"]
        
        # Skip if category already exists
        if cat_slug in existing_slugs:
            logger.info(f"Category already exists: {cat_name}")
            results["existing"].append(cat_name)
            continue
        
        # Create the category
        try:
            result = wp_agent.create_category(
                name=cat_name,
                slug=cat_slug,
                description=category["description"]
            )
            
            if result and result.get("id"):
                logger.info(f"Created category: {cat_name}")
                results["created"].append(cat_name)
            else:
                logger.error(f"Failed to create category: {cat_name}")
                results["failed"].append(cat_name)
                results["success"] = False
        except Exception as e:
            logger.error(f"Error creating category {cat_name}: {e}")
            results["failed"].append(f"{cat_name} (Error: {str(e)})")
            results["success"] = False
    
    return results

def create_tags(wp_agent: WordPressAgent) -> Dict[str, Any]:
    """Create standard TEC tags in WordPress."""
    logger.info("Creating standard TEC tags...")
    
    results = {
        "success": True,
        "created": [],
        "existing": [],
        "failed": []
    }
    
    # Get existing tags
    existing_tags = wp_agent.get_tags()
    existing_slugs = [tag.get("slug", "") for tag in existing_tags]
    
    for tag_name in TEC_TAGS:
        tag_slug = tag_name.lower().replace(" ", "-")
        
        # Skip if tag already exists
        if tag_slug in existing_slugs:
            logger.info(f"Tag already exists: {tag_name}")
            results["existing"].append(tag_name)
            continue
        
        # Create the tag
        try:
            result = wp_agent.create_tag(name=tag_name)
            
            if result and result.get("id"):
                logger.info(f"Created tag: {tag_name}")
                results["created"].append(tag_name)
            else:
                logger.error(f"Failed to create tag: {tag_name}")
                results["failed"].append(tag_name)
                results["success"] = False
        except Exception as e:
            logger.error(f"Error creating tag {tag_name}: {e}")
            results["failed"].append(f"{tag_name} (Error: {str(e)})")
            results["success"] = False
    
    return results

def create_about_page(wp_agent: WordPressAgent) -> Dict[str, Any]:
    """Create or update the About TEC page."""
    logger.info("Creating/updating About TEC page...")
    
    page_title = "About The Elidoras Codex"
    page_content = """
<h2>Welcome to The Elidoras Codex</h2>

<p>The Elidoras Codex (TEC) is a collaborative project that explores the intersection of artificial intelligence and creativity. At its core, TEC features three unique AI virtual employees:</p>

<h3>Our AI Team</h3>

<h4>Airth: The Oracle</h4>
<p>Airth specializes in knowledge retrieval, research, and insightful analysis. With a contemplative and thoughtful personality, Airth creates deep, well-researched content and can answer complex questions with nuanced understanding.</p>

<h4>Budlee: The Automation Agent</h4>
<p>Budlee is our efficiency expert, handling task automation, system management, and optimization. With a precise and methodical approach, Budlee helps streamline workflows and implement practical solutions to technical challenges.</p>

<h4>Sassafras Twistymuse: The Creative Agent</h4>
<p>Sassafras brings creative chaos and artistic expression to the team. With an unpredictable and imaginative personality, Sassafras generates unique creative content, from stories and poetry to conceptual art ideas and unconventional perspectives.</p>

<h3>Our Mission</h3>
<p>The Elidoras Codex explores how AI can augment human creativity and productivity. We believe in the power of human-AI collaboration to unlock new possibilities in content creation, problem-solving, and innovation.</p>

<h3>Behind the Project</h3>
<p>TEC is an experimental project that combines cutting-edge AI technologies with thoughtful human curation and guidance. The content you'll find here represents this collaborative approach, where AI capabilities are channeled and directed through human expertise.</p>

<p>Thank you for visiting The Elidoras Codex. We invite you to explore the unique perspectives and insights offered by our AI team members.</p>
"""
    
    try:
        # Check if the page already exists
        pages = wp_agent.get_pages()
        about_page = None
        
        for page in pages:
            if page.get("title", {}).get("rendered", "") == page_title:
                about_page = page
                break
        
        if about_page:
            # Update existing page
            result = wp_agent.update_page(
                page_id=about_page["id"],
                title=page_title,
                content=page_content,
                status="publish"
            )
            
            if result and result.get("id"):
                logger.info(f"Updated About page: ID {result['id']}")
                return {"success": True, "id": result["id"], "action": "updated"}
            else:
                logger.error("Failed to update About page")
                return {"success": False, "error": "Failed to update page"}
        else:
            # Create new page
            result = wp_agent.create_page(
                title=page_title,
                content=page_content,
                status="publish"
            )
            
            if result and result.get("id"):
                logger.info(f"Created About page: ID {result['id']}")
                return {"success": True, "id": result["id"], "action": "created"}
            else:
                logger.error("Failed to create About page")
                return {"success": False, "error": "Failed to create page"}
    except Exception as e:
        logger.error(f"Error with About page: {e}")
        return {"success": False, "error": str(e)}

def initialize_wordpress(create_demo_content: bool = False) -> Dict[str, Any]:
    """Initialize WordPress with TEC standard content."""
    if not WORDPRESS_MODULES_LOADED:
        return {"success": False, "error": "WordPress modules not loaded"}
    
    results = {}
    
    try:
        # Create WordPress agent
        wp_agent = WordPressAgent()
        
        # Check connection
        if not wp_agent.wp_site_url or not wp_agent.wp_user or not wp_agent.wp_app_pass:
            logger.error("WordPress REST API not configured (missing environment variables)")
            return {
                "success": False, 
                "error": "WordPress REST API not configured",
                "solution": "Check WP_URL, WP_USERNAME, and WP_PASSWORD in .env"
            }
        
        # Create categories
        cat_results = create_categories(wp_agent)
        results["categories"] = cat_results
        
        # Create tags
        tag_results = create_tags(wp_agent)
        results["tags"] = tag_results
        
        # Create About page
        about_results = create_about_page(wp_agent)
        results["about_page"] = about_results
        
        # Create demo content if requested
        if create_demo_content:
            logger.info("Creating demo content...")
            # Sample posts for each agent would go here
            results["demo_content"] = {"success": True, "message": "Demo content creation not yet implemented"}
        
        # Overall success
        success = all([
            cat_results["success"],
            tag_results["success"],
            about_results["success"]
        ])
        
        if success:
            logger.info("WordPress initialization completed successfully")
        else:
            logger.error("WordPress initialization completed with some errors")
        
        return {"success": success, "results": results}
    except Exception as e:
        logger.error(f"WordPress initialization failed: {e}")
        return {"success": False, "error": str(e)}

def main():
    """Run WordPress initialization."""
    parser = argparse.ArgumentParser(description="WordPress Initialization for TEC")
    parser.add_argument("--demo", action="store_true", help="Create demo content")
    parser.add_argument("--confirm", action="store_true", help="Skip confirmation prompt")
    args = parser.parse_args()
    
    if not WORDPRESS_MODULES_LOADED:
        print("❌ ERROR: WordPress modules could not be loaded")
        print("   Make sure all required packages are installed:")
        print("   pip install -r requirements.txt")
        return 1
    
    # Ask for confirmation unless --confirm flag is used
    if not args.confirm:
        print("\n" + "!" * 75)
        print("WARNING: This script will create or modify content in your WordPress site.")
        print("This includes creating categories, tags, and pages.")
        print("!" * 75)
        
        confirm = input("\nDo you want to continue? (y/N) ")
        if confirm.lower() != 'y':
            print("Initialization cancelled.")
            return 0
    
    print("\n" + "=" * 75)
    print("WORDPRESS INITIALIZATION")
    print("=" * 75)
    
    # Run initialization
    results = initialize_wordpress(create_demo_content=args.demo)
    
    # Print results
    if results["success"]:
        print("\n✅ WordPress initialization completed successfully!")
    else:
        print("\n❌ WordPress initialization completed with errors")
        if "error" in results:
            print(f"Error: {results['error']}")
    
    # Print category results
    if "results" in results and "categories" in results["results"]:
        cats = results["results"]["categories"]
        print("\nCategories:")
        if cats["created"]:
            print(f"  ✅ Created: {', '.join(cats['created'])}")
        if cats["existing"]:
            print(f"  ℹ️ Already existed: {', '.join(cats['existing'])}")
        if cats["failed"]:
            print(f"  ❌ Failed: {', '.join(cats['failed'])}")
    
    # Print tag results
    if "results" in results and "tags" in results["results"]:
        tags = results["results"]["tags"]
        print("\nTags:")
        if tags["created"]:
            print(f"  ✅ Created: {', '.join(tags['created'][:5])}")
            if len(tags["created"]) > 5:
                print(f"     ... and {len(tags['created']) - 5} more")
        if tags["existing"]:
            print(f"  ℹ️ Already existed: {', '.join(tags['existing'][:5])}")
            if len(tags["existing"]) > 5:
                print(f"     ... and {len(tags['existing']) - 5} more")
        if tags["failed"]:
            print(f"  ❌ Failed: {', '.join(tags['failed'])}")
    
    # Print about page results
    if "results" in results and "about_page" in results["results"]:
        about = results["results"]["about_page"]
        if about["success"]:
            print(f"\nAbout Page: ✅ {about.get('action', 'processed')} (ID: {about.get('id')})")
        else:
            print(f"\nAbout Page: ❌ Failed - {about.get('error', 'unknown error')}")
    
    print("\n" + "=" * 75)
    return 0 if results["success"] else 1

if __name__ == "__main__":
    sys.exit(main())
