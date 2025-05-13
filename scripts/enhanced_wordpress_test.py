#!/usr/bin/env python3
"""
Enhanced WordPress Integration Test for TEC_OFFICE_REPO.
This comprehensive script tests all WordPress integrations and utilities.
"""
import os
import sys
import json
import logging
import argparse
import time
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("TEC.WordPressTest")

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables
load_dotenv(os.path.join('config', '.env'))

# Import the WordPress components
try:
    from src.wordpress.wordpress_xmlrpc import WordPressXMLRPC, test_wordpress_connection
    from src.wordpress.utils import WordPressCache, WordPressContentTools, test_wordpress_tools
    from src.agents.wp_poster import WordPressAgent
    WORDPRESS_MODULES_LOADED = True
except ImportError as e:
    logger.error(f"Failed to import WordPress modules: {e}")
    WORDPRESS_MODULES_LOADED = False

class TestResult:
    """Simple class to track test results."""
    
    def __init__(self):
        self.total = 0
        self.passed = 0
        self.results = {}
        
    def add_result(self, name: str, result: Dict[str, Any]):
        """Add a test result."""
        success = bool(result.get("success", False))
        self.total += 1
        if success:
            self.passed += 1
            
        self.results[name] = {
            "success": success,
            **result
        }
        
    def print_result(self, name: str):
        """Print a specific test result."""
        if name not in self.results:
            print(f"Test '{name}' not found in results.")
            return
            
        result = self.results[name]
        status = "✅ PASSED" if result["success"] else "❌ FAILED"
        
        print(f"\n{'-' * 60}")
        print(f"TEST: {name}")
        print(f"{'-' * 60}")
        print(f"Result: {status}")
        
        # Print other result details
        for key, value in result.items():
            if key != "success":
                print(f"{key}: {value}")
    
    def print_summary(self):
        """Print a summary of all test results."""
        print(f"\n{'=' * 75}")
        print(f"WORDPRESS INTEGRATION TEST SUMMARY")
        print(f"{'=' * 75}")
        print(f"Tests Run: {self.total}")
        print(f"Tests Passed: {self.passed}")
        print(f"Tests Failed: {self.total - self.passed}")
        print(f"Success Rate: {self.passed/self.total*100:.1f}%")
        print(f"{'=' * 75}")
        
        # Print individual test results
        for name, result in self.results.items():
            status = "✅ PASSED" if result["success"] else "❌ FAILED"
            print(f"{status} - {name}")
        
        print(f"{'=' * 75}")

def test_xmlrpc_connection() -> Dict[str, Any]:
    """Test the XML-RPC connection to WordPress."""
    if not WORDPRESS_MODULES_LOADED:
        return {"success": False, "error": "WordPress modules not loaded"}
        
    try:
        logger.info("Testing WordPress XML-RPC connection...")
        wp = WordPressXMLRPC()
        
        # Test connection
        connected = wp.is_connected()
        
        if connected:
            logger.info(f"Successfully connected to {wp.site_url}")
            
            # Try to get recent posts as additional test
            posts = wp.get_posts(1)
            posts_retrieved = len(posts) > 0
            
            return {
                "success": True,
                "site_url": wp.site_url,
                "posts_retrieved": posts_retrieved,
                "message": "XML-RPC connection successful"
            }
        else:
            logger.error("Failed to connect via XML-RPC")
            return {
                "success": False,
                "site_url": wp.site_url if wp.site_url else "Not configured",
                "message": "XML-RPC connection failed"
            }
    except Exception as e:
        logger.error(f"Error testing XML-RPC connection: {e}")
        return {"success": False, "error": str(e)}

def test_rest_api_connection() -> Dict[str, Any]:
    """Test the REST API connection through the agent."""
    if not WORDPRESS_MODULES_LOADED:
        return {"success": False, "error": "WordPress modules not loaded"}
        
    try:
        logger.info("Testing WordPress REST API connection...")
        wp_agent = WordPressAgent()
        
        # Check if the agent is configured
        if not wp_agent.wp_site_url or not wp_agent.wp_user or not wp_agent.wp_app_pass:
            logger.error("WordPress REST API not configured (missing environment variables)")
            return {
                "success": False, 
                "error": "WordPress REST API not configured",
                "solution": "Check WP_URL, WP_USERNAME, and WP_PASSWORD in .env"
            }
        
        # Test connection by getting categories
        categories = wp_agent.get_categories()
        
        if categories:
            logger.info(f"Successfully retrieved {len(categories)} categories")
            return {
                "success": True,
                "site_url": wp_agent.wp_site_url,
                "categories": len(categories),
                "message": "REST API connection successful"
            }
        else:
            logger.error("Failed to retrieve categories from WordPress")
            return {
                "success": False,
                "site_url": wp_agent.wp_site_url,
                "message": "Failed to retrieve categories"
            }
    except Exception as e:
        logger.error(f"REST API connection failed: {e}")
        return {"success": False, "error": str(e)}

def test_create_draft_post() -> Dict[str, Any]:
    """Test creating a draft post using both methods."""
    if not WORDPRESS_MODULES_LOADED:
        return {"success": False, "error": "WordPress modules not loaded"}
        
    results = {
        "xmlrpc": {"success": False, "method": "xmlrpc"},
        "rest": {"success": False, "method": "rest"}
    }
    
    # Generate a test post title and content
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    title = f"TEC Test Post - {timestamp}"
    content = f"""<p>This is a test post created by the TEC WordPress integration test script.</p>
<p>Timestamp: {timestamp}</p>
<p>This post was created to verify WordPress integration functionality.</p>"""

    # Test using XML-RPC
    logger.info("Creating draft post using XML-RPC...")
    try:
        wp_xmlrpc = WordPressXMLRPC()
        if not wp_xmlrpc.client:
            logger.error("WordPress XML-RPC client not initialized")
            results["xmlrpc"]["error"] = "WordPress XML-RPC client not initialized"
        else:
            xmlrpc_result = wp_xmlrpc.create_post(
                title=f"{title} (XML-RPC)",
                content=content,
                categories=["Test"],
                tags=["test", "tec", "automation"],
                status="draft"
            )
            
            if xmlrpc_result.get("success"):
                logger.info(f"XML-RPC draft post created: ID {xmlrpc_result.get('post_id')}")
                results["xmlrpc"] = {
                    "success": True,
                    "post_id": xmlrpc_result.get("post_id"),
                    "url": xmlrpc_result.get("url"),
                    "method": "xmlrpc"
                }
            else:
                logger.error(f"Failed to create XML-RPC draft post: {xmlrpc_result.get('error')}")
                results["xmlrpc"]["error"] = xmlrpc_result.get("error")
    except Exception as e:
        logger.error(f"XML-RPC draft post creation failed: {e}")
        results["xmlrpc"]["error"] = str(e)
    
    # Test using REST API
    logger.info("Creating draft post using REST API...")
    try:
        wp_agent = WordPressAgent()
        rest_result = wp_agent.create_post(
            title=f"{title} (REST API)",
            content=content,
            category="Test",
            tags=["test", "tec", "automation", "rest-api"],
            status="draft"
        )
        
        if rest_result.get("success"):
            logger.info(f"REST API draft post created: ID {rest_result.get('post_id')}")
            results["rest"] = {
                "success": True,
                "post_id": rest_result.get("post_id"),
                "url": rest_result.get("url"),
                "method": "rest"
            }
        else:
            logger.error(f"Failed to create REST API draft post: {rest_result.get('error')}")
            results["rest"]["error"] = rest_result.get("error")
    except Exception as e:
        logger.error(f"REST API draft post creation failed: {e}")
        results["rest"]["error"] = str(e)
    
    # Combine results
    overall_success = results["xmlrpc"]["success"] or results["rest"]["success"]
    return {
        "success": overall_success,
        "xmlrpc": results["xmlrpc"],
        "rest": results["rest"],
        "message": "Post creation test completed"
    }

def test_wordpress_utilities() -> Dict[str, Any]:
    """Test WordPress utility functions."""
    if not WORDPRESS_MODULES_LOADED:
        return {"success": False, "error": "WordPress modules not loaded"}
        
    try:
        logger.info("Testing WordPress utilities...")
        
        # Test the cache functionality
        cache_test = {"success": False}
        try:
            cache = WordPressCache(ttl_seconds=10)
            cache.set("test_key", "test_value")
            retrieved_value = cache.get("test_key")
            
            cache_test = {
                "success": retrieved_value == "test_value",
                "retrieved_value": retrieved_value
            }
            
            # Test expiration
            logger.info("Testing cache expiration (waiting 11 seconds)...")
            time.sleep(11)  # Wait for cache to expire
            expired_value = cache.get("test_key")
            
            cache_test["expiration_test_success"] = expired_value is None
            cache_test["expired_value"] = expired_value
            
            cache.clear()
        except Exception as e:
            logger.error(f"Cache test failed: {e}")
            cache_test["error"] = str(e)
            
        # Test content optimization
        content_test = {"success": False}
        try:
            test_content = "This is a test paragraph.\n\nThis is another paragraph."
            optimized = WordPressContentTools.optimize_html_content(test_content)
            
            content_test = {
                "success": '<p>' in optimized,
                "optimized_content": optimized[:50] + "..." if len(optimized) > 50 else optimized
            }
            
            # Test image extraction
            img_content = '<img src="https://example.com/image.jpg"> <img src="https://example.com/image2.png">'
            images = WordPressContentTools.extract_images_from_content(img_content)
            
            content_test["image_extraction_success"] = len(images) == 2
            content_test["extracted_images"] = images
        except Exception as e:
            logger.error(f"Content optimization test failed: {e}")
            content_test["error"] = str(e)
            
        # Return combined results
        overall_success = cache_test["success"] and content_test["success"]
        return {
            "success": overall_success,
            "cache_test": cache_test,
            "content_test": content_test,
            "message": "WordPress utilities test completed"
        }
    except Exception as e:
        logger.error(f"WordPress utilities test error: {e}")
        return {"success": False, "error": str(e)}

def print_troubleshooting_tips():
    """Print troubleshooting tips for WordPress connection issues."""
    print("\n" + "=" * 75)
    print("TROUBLESHOOTING TIPS")
    print("=" * 75)
    print("1. Check environment variables in config/.env:")
    print("   - WP_URL: Should include the full URL to your WordPress site")
    print("   - WP_USERNAME: Your WordPress username")
    print("   - WP_PASSWORD: Your WordPress application password")
    print("\n2. WordPress XML-RPC issues:")
    print("   - Ensure XML-RPC is enabled on your WordPress site")
    print("   - Check if your hosting provider blocks XML-RPC requests")
    print("   - Try using the REST API integration instead")
    print("\n3. WordPress REST API issues:")
    print("   - Verify your application password has the correct permissions")
    print("   - Check if the REST API is enabled and not blocked by security plugins")
    print("   - Ensure your site is using HTTPS if required by your hosting")
    print("\n4. General issues:")
    print("   - Check WordPress version (5.0+ recommended)")
    print("   - Verify network connectivity to your WordPress site")
    print("   - Check for security plugins that might be blocking API access")
    print("=" * 75)

def main():
    """Run WordPress integration tests based on command line arguments."""
    parser = argparse.ArgumentParser(
        description="Enhanced WordPress Integration Test for TEC_OFFICE_REPO",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/enhanced_wordpress_test.py --all
  python scripts/enhanced_wordpress_test.py --connection
  python scripts/enhanced_wordpress_test.py --create-post --utilities
        """
    )
    
    # Add test selection options
    parser.add_argument("--all", action="store_true", help="Run all WordPress integration tests")
    parser.add_argument("--connection", action="store_true", help="Test WordPress basic connection")
    parser.add_argument("--xmlrpc", action="store_true", help="Test XML-RPC connection specifically")
    parser.add_argument("--rest-api", action="store_true", help="Test REST API connection specifically")
    parser.add_argument("--create-post", action="store_true", help="Test creating draft posts")
    parser.add_argument("--utilities", action="store_true", help="Test WordPress utility functions")
    parser.add_argument("--troubleshooting", action="store_true", help="Show troubleshooting tips")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show more detailed output")
    
    args = parser.parse_args()
    
    # Show troubleshooting tips if requested
    if args.troubleshooting:
        print_troubleshooting_tips()
        return 0
    
    # If no tests specified, run all
    run_all = args.all or not any([
        args.connection, args.xmlrpc, args.rest_api,
        args.create_post, args.utilities
    ])
    
    if not WORDPRESS_MODULES_LOADED:
        print("❌ ERROR: WordPress modules could not be loaded")
        print("   Make sure all required packages are installed:")
        print("   pip install -r requirements.txt")
        return 1
    
    # Initialize test results tracking
    results = TestResult()
    
    # Run selected tests
    print("\n" + "=" * 75)
    print("WORDPRESS INTEGRATION TEST")
    print("=" * 75)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 75)
    
    # Connection tests
    if run_all or args.connection or args.xmlrpc:
        xmlrpc_result = test_xmlrpc_connection()
        results.add_result("XML-RPC Connection", xmlrpc_result)
        
    if run_all or args.connection or args.rest_api:
        rest_result = test_rest_api_connection()
        results.add_result("REST API Connection", rest_result)
    
    # Post creation test
    if run_all or args.create_post:
        post_result = test_create_draft_post()
        results.add_result("Draft Post Creation", post_result)
    
    # WordPress utilities test
    if run_all or args.utilities:
        utils_result = test_wordpress_utilities()
        results.add_result("WordPress Utilities", utils_result)
    
    # Print final summary
    results.print_summary()
    
    # If there were failures and verbose mode is on, print detailed results
    if args.verbose:
        print("\nDetailed test results:")
        for name in results.results:
            results.print_result(name)
    
    # Show troubleshooting tips if any tests failed
    if results.total - results.passed > 0:
        print_troubleshooting_tips()
    
    # Return success if all tests passed
    return 0 if results.passed == results.total else 1

if __name__ == "__main__":
    sys.exit(main())
