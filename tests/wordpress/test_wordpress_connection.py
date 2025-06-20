#!/usr/bin/env python3
"""
Test WordPress connection for The Elidoras Codex.
This script verifies WordPress credentials and tests various API operations.
"""
import os
import sys
import json
import logging
import argparse
import pytest
from typing import Dict, Any
from pathlib import Path

# Import test utilities
sys.path.append(str(Path(__file__).parent.parent))
from test_utils import load_test_env, get_test_config, load_test_data

# Configure logging
logger = logging.getLogger("TEC.WordPressTest")

# Load environment variables
load_test_env()

# Import the WordPress components
try:
    from src.wordpress import test_wordpress_connection as check_wordpress_connection
    from src.wordpress.wordpress_xmlrpc import WordPressXMLRPC
    from src.agents.wp_poster import WordPressAgent
    WORDPRESS_MODULES_LOADED = True
except ImportError as e:
    logger.error(f"Failed to import WordPress modules: {e}")
    WORDPRESS_MODULES_LOADED = False

def test_connection():
    """Test the basic WordPress connection."""
    if not WORDPRESS_MODULES_LOADED:
        pytest.skip("WordPress modules not loaded")
    
    logger.info("Testing WordPress connection...")
    result = check_wordpress_connection()
    logger.info(f"Connection test result: {result['success']}")
    assert result['success'], f"WordPress connection failed: {result.get('error', 'Unknown error')}"

def test_create_post(title: str = "TEC WordPress Test Post", 
                    content: str = "<p>This is a test post from the TEC WordPress integration.</p>",
                    draft: bool = True):
    """Test creating a post in WordPress."""
    if not WORDPRESS_MODULES_LOADED:
        pytest.skip("WordPress modules not loaded")
        
    # Use the WordPress agent for creating posts
    logger.info("Creating test post using WordPressAgent...")
    agent = WordPressAgent(os.path.join('config'))
    
    # Status should be 'draft' for testing purposes
    status = "draft" if draft else "publish"
    
    # Create the post
    result = agent.create_post(
        title=title,
        content=content,
        category="uncategorized",
        tags=["test", "tec-integration"],
        status=status
    )
    
    if result.get("success"):
        logger.info(f"Successfully created post with ID {result.get('post_id')}")
    else:
        logger.error(f"Failed to create post: {result.get('error')}")
        
    assert result.get("success"), f"Failed to create post: {result.get('error', 'Unknown error')}"

def test_xmlrpc_connection():
    """Test the XML-RPC connection to WordPress."""
    if not WORDPRESS_MODULES_LOADED:
        pytest.skip("WordPress modules not loaded")
        
    logger.info("Testing WordPress XML-RPC connection...")
    wp = WordPressXMLRPC()
    
    # Test connection
    connected = wp.is_connected()
    
    if connected:
        logger.info(f"Successfully connected to {wp.site_url}")
        
        # Try to get recent posts as additional test
        posts = wp.get_posts(1)
        posts_retrieved = len(posts) > 0
        
        assert True, "XML-RPC connection successful"
    else:
        logger.error("Failed to connect via XML-RPC")
        assert False, f"XML-RPC connection failed to {wp.site_url}"

def print_test_result(name: str, result: Dict[str, Any]) -> None:
    """Print a formatted test result."""
    print(f"\n{'=' * 50}")
    print(f"TEST: {name}")
    print(f"{'=' * 50}")
    
    if result.get("success"):
        print("✅ SUCCESS")
    else:
        print("❌ FAILED")
        
    # Print result details
    for key, value in result.items():
        if key != "success":
            print(f"{key}: {value}")

def run_all_tests(draft: bool = True) -> bool:
    """Run all WordPress tests."""
    # Test basic connection
    connection_result = test_connection()
    print_test_result("Basic WordPress Connection", connection_result)
    
    if not connection_result.get("success"):
        print("\nTroubleshooting tips:")
        print("1. Check that WP_URL, WP_USERNAME, and WP_PASSWORD are set in config/.env")
        print("2. Ensure that the WordPress site has XML-RPC enabled")
        print("3. Verify that the application password has sufficient permissions")
        print("4. Check if the WordPress site is accessible from this machine")
        return False
        
    # Test XML-RPC connection
    xmlrpc_result = test_xmlrpc_connection()
    print_test_result("WordPress XML-RPC Connection", xmlrpc_result)
    
    # Test creating a post
    post_result = test_create_post(draft=draft)
    print_test_result("Create WordPress Post", post_result)
    
    # Overall success
    all_success = all([
        connection_result.get("success", False),
        xmlrpc_result.get("success", False),
        post_result.get("success", False)
    ])
    
    print(f"\n{'=' * 50}")
    if all_success:
        print("✅ ALL WORDPRESS TESTS PASSED")
    else:
        print("❌ SOME WORDPRESS TESTS FAILED")
    print(f"{'=' * 50}")
    
    return all_success

def main():
    """Test the WordPress connection."""
    parser = argparse.ArgumentParser(description='Test WordPress Connection')
    parser.add_argument('--publish', action='store_true', 
                      help='Publish test posts instead of saving as drafts')
    parser.add_argument('--test', choices=['connection', 'xmlrpc', 'post', 'all'],
                      default='all', help='Specific test to run')
    
    args = parser.parse_args()
    
    if not WORDPRESS_MODULES_LOADED:
        print("❌ ERROR: WordPress modules could not be loaded")
        return 1
    
    if args.test == 'connection':
        result = test_connection()
        print_test_result("WordPress Connection", result)
        return 0 if result.get("success") else 1
    elif args.test == 'xmlrpc':
        result = test_xmlrpc_connection()
        print_test_result("WordPress XML-RPC", result)
        return 0 if result.get("success") else 1
    elif args.test == 'post':
        result = test_create_post(draft=not args.publish)
        print_test_result("Create WordPress Post", result)
        return 0 if result.get("success") else 1
    else:
        # Run all tests
        success = run_all_tests(draft=not args.publish)
        return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
