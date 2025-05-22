#!/usr/bin/env python3
"""
Test script for the duplicate article detection feature.
This script will test the duplicate detection by:
1. Fetching existing posts from WordPress
2. Creating a new article with a title similar to an existing one
3. Testing whether the duplicate detection works
"""
import os
import sys
import logging
from datetime import datetime

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
    ]
)
logger = logging.getLogger("DuplicateDetectionTest")

# Import necessary modules
try:
    from src.agents.wp_poster import WordPressAgent
except ImportError as e:
    logger.critical(f"Failed to import required modules: {e}")
    sys.exit(1)

def main():
    """Test the duplicate detection functionality."""
    print("\n=== Airth Duplicate Article Detection Test ===\n")

    # Initialize the WordPress agent
    wp_agent = WordPressAgent()
    
    # Create an adapter similar to the one in AirthNewsAutomation
    class TestAdapter:
        def __init__(self, wp_agent):
            self.wp_agent = wp_agent
        
        def check_for_duplicate_article(self, title, content=None, similarity_threshold=0.7):
            """Check if a similar article already exists."""
            try:
                # Get recent posts from WordPress
                existing_posts = self.wp_agent.get_posts(per_page=20)
                
                if not existing_posts:
                    print("No existing posts found in WordPress")
                    return False, None
                
                # Normalize the new title for comparison
                import re
                from difflib import SequenceMatcher
                
                def normalize_title(title_text):
                    return re.sub(r'[^\w\s]', '', title_text.lower()).strip()
                
                def calculate_similarity(text1, text2):
                    return SequenceMatcher(None, text1, text2).ratio()
                
                normalized_new_title = normalize_title(title)
                
                print(f"\nChecking for duplicates of: '{title}'\n")
                print("Existing posts:")
                
                # Check each existing post for similarity
                for post in existing_posts:
                    existing_title = post.get("title", {}).get("rendered", "")
                    if not existing_title:
                        continue
                    
                    # Compare normalized titles
                    normalized_existing_title = normalize_title(existing_title)
                    similarity = calculate_similarity(normalized_new_title, normalized_existing_title)
                    
                    # Print all similarity scores for inspection
                    print(f"- '{existing_title}' (similarity: {similarity:.2%})")
                    
                    # If similarity exceeds threshold, consider it a duplicate
                    if similarity > similarity_threshold:
                        print(f"\nDUPLICATE DETECTED: Match with '{existing_title}' (similarity: {similarity:.2%})")
                        return True, {
                            "id": post.get("id"),
                            "title": existing_title,
                            "link": post.get("link"),
                            "similarity": similarity
                        }
                
                print("\nNo duplicates found above threshold.")
                return False, None
                    
            except Exception as e:
                print(f"Error checking for duplicate articles: {e}")
                return False, None

    # Initialize the test adapter
    adapter = TestAdapter(wp_agent)

    # Test case 1: Check an exact duplicate
    print("\n=== Test Case 1: Exact Duplicate ===")
    # Fetch one existing post to use as a reference
    existing_posts = wp_agent.get_posts(per_page=1)
    if existing_posts:
        reference_post = existing_posts[0]
        reference_title = reference_post.get("title", {}).get("rendered", "")
        print(f"Reference post title: {reference_title}")

        # Test with the exact same title
        is_duplicate, info = adapter.check_for_duplicate_article(reference_title)
        print(f"Result: {'DUPLICATE' if is_duplicate else 'NOT DUPLICATE'}")
    else:
        print("No existing posts to test with.")

    # Test case 2: Similar but not identical
    print("\n=== Test Case 2: Similar Title ===")
    if existing_posts:
        reference_title = reference_post.get("title", {}).get("rendered", "")
        # Create a similar title by appending text
        similar_title = f"{reference_title} - Updated"
        print(f"Testing with similar title: {similar_title}")

        # Test with a similar title
        is_duplicate, info = adapter.check_for_duplicate_article(similar_title, similarity_threshold=0.8)
        print(f"Result: {'DUPLICATE' if is_duplicate else 'NOT DUPLICATE'}")

    # Test case 3: Completely different title
    print("\n=== Test Case 3: Different Title ===")
    different_title = f"Completely Unique Article Title {datetime.now().strftime('%Y%m%d%H%M%S')}"
    print(f"Testing with different title: {different_title}")

    # Test with a different title
    is_duplicate, info = adapter.check_for_duplicate_article(different_title)
    print(f"Result: {'DUPLICATE' if is_duplicate else 'NOT DUPLICATE'}")

    print("\n=== Test Complete ===")

if __name__ == "__main__":
    main()
