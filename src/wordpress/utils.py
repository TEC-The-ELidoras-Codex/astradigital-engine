"""
WordPress Integration Utilities for The Elidoras Codex.
This module provides additional tools for working with WordPress sites.
"""
import os
import logging
import json
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
import re
import time

# Configure logging
logger = logging.getLogger("TEC.WordPress.Utils")

# Import WordPress XML-RPC client
try:
    from .wordpress_xmlrpc import WordPressXMLRPC
except ImportError:
    logger.warning("WordPress XML-RPC module not found. Some WordPress utilities may not work.")

class WordPressCache:
    """
    Simple cache for WordPress data to reduce API calls.
    """
    
    def __init__(self, cache_file: str = None, ttl_seconds: int = 3600):
        """
        Initialize the WordPress cache.
        
        Args:
            cache_file: Path to the cache file
            ttl_seconds: Time-to-live for cache entries in seconds (default: 1 hour)
        """
        self.cache_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'cache')
        
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir, exist_ok=True)
            
        self.cache_file = cache_file or os.path.join(self.cache_dir, 'wp_cache.json')
        self.ttl_seconds = ttl_seconds
        self.cache = {}
        
        # Load cache from file if it exists
        self._load_cache()
        
    def _load_cache(self):
        """Load cache from file if it exists."""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r') as f:
                    self.cache = json.load(f)
                logger.debug(f"Loaded WordPress cache from {self.cache_file}")
        except Exception as e:
            logger.error(f"Error loading WordPress cache: {e}")
            self.cache = {}
            
    def _save_cache(self):
        """Save cache to file."""
        try:
            with open(self.cache_file, 'w') as f:
                json.dump(self.cache, f)
            logger.debug(f"Saved WordPress cache to {self.cache_file}")
        except Exception as e:
            logger.error(f"Error saving WordPress cache: {e}")
            
    def get(self, key: str) -> Optional[Any]:
        """
        Get a value from the cache if it exists and hasn't expired.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found or expired
        """
        if key not in self.cache:
            return None
            
        item = self.cache[key]
        timestamp = item.get('timestamp', 0)
        value = item.get('value')
        
        # Check if the item has expired
        if time.time() - timestamp > self.ttl_seconds:
            logger.debug(f"Cache item expired: {key}")
            return None
            
        logger.debug(f"Cache hit: {key}")
        return value
        
    def set(self, key: str, value: Any):
        """
        Set a value in the cache.
        
        Args:
            key: Cache key
            value: Value to cache
        """
        self.cache[key] = {
            'timestamp': time.time(),
            'value': value
        }
        logger.debug(f"Cache set: {key}")
        self._save_cache()
        
    def clear(self):
        """Clear the entire cache."""
        self.cache = {}
        self._save_cache()
        logger.debug("Cache cleared")
        
    def remove(self, key: str):
        """
        Remove an item from the cache.
        
        Args:
            key: Cache key to remove
        """
        if key in self.cache:
            del self.cache[key]
            self._save_cache()
            logger.debug(f"Removed from cache: {key}")


class WordPressContentTools:
    """
    Tools for processing and optimizing WordPress content.
    """
    
    @staticmethod
    def optimize_html_content(content: str) -> str:
        """
        Optimize HTML content for WordPress.
        
        Args:
            content: HTML content
            
        Returns:
            Optimized HTML content
        """
        # Make sure paragraphs have proper HTML tags
        if not content.strip().startswith('<'):
            lines = content.split('\n\n')
            formatted_lines = []
            
            for line in lines:
                if line.strip():
                    # Skip if line already has HTML tags
                    if re.match(r'^\s*<\w+', line):
                        formatted_lines.append(line)
                    else:
                        # Wrap plain text in paragraph tags
                        formatted_lines.append(f'<p>{line.strip()}</p>')
                        
            content = '\n'.join(formatted_lines)
            
        # Make sure headings have proper hierarchy (start with H2, not H1)
        content = re.sub(r'<h1([^>]*)>(.*?)</h1>', r'<h2\1>\2</h2>', content)
        
        # Add alt text placeholders for images without alt text
        content = re.sub(r'<img([^>]*?)alt=""([^>]*?)>', r'<img\1alt="TEC Generated Image"\2>', content)
        content = re.sub(r'<img(?![^>]*?alt=)([^>]*?)>', r'<img\1 alt="TEC Generated Image">', content)
        
        return content
    
    @staticmethod
    def extract_images_from_content(content: str) -> List[str]:
        """
        Extract image URLs from HTML content.
        
        Args:
            content: HTML content
            
        Returns:
            List of image URLs
        """
        image_urls = []
        img_regex = r'src="(https?://[^"]+\.(jpg|jpeg|png|gif|webp))"'
        
        for match in re.finditer(img_regex, content):
            image_urls.append(match.group(1))
            
        return image_urls
    
    @staticmethod
    def sanitize_title(title: str) -> str:
        """
        Sanitize a post title.
        
        Args:
            title: Post title
            
        Returns:
            Sanitized title
        """
        # Remove excessive whitespace
        title = ' '.join(title.strip().split())
        
        # Max length for WordPress titles (practical limit)
        if len(title) > 100:
            title = title[:97] + '...'
            
        return title
    
    @staticmethod
    def generate_slug(title: str) -> str:
        """
        Generate a URL slug from a title.
        
        Args:
            title: Post title
            
        Returns:
            URL slug
        """
        # Convert to lowercase
        slug = title.lower()
        
        # Remove special characters
        slug = re.sub(r'[^\w\s-]', '', slug)
        
        # Replace spaces with hyphens
        slug = re.sub(r'\s+', '-', slug)
        
        # Remove consecutive hyphens
        slug = re.sub(r'-+', '-', slug)
        
        # Trim to reasonable length
        if len(slug) > 60:
            slug = slug[:60].rstrip('-')
            
        return slug
    
    @staticmethod
    def format_for_seo(title: str, content: str) -> Dict[str, str]:
        """
        Format title and content for SEO optimization.
        
        Args:
            title: Post title
            content: Post content
            
        Returns:
            Dictionary with SEO-optimized title and excerpt
        """
        # Create SEO-friendly title (max 60 chars)
        seo_title = title
        if len(seo_title) > 60:
            seo_title = seo_title[:57] + '...'
            
        # Create excerpt (max 160 chars)
        # Strip HTML tags
        text_content = re.sub(r'<[^>]+>', '', content)
        excerpt = ' '.join(text_content.split())[:157] + '...'
        
        return {
            'seo_title': seo_title,
            'excerpt': excerpt
        }


def test_wordpress_tools() -> Dict[str, Any]:
    """
    Test the WordPress utilities.
    
    Returns:
        Dictionary with test results
    """
    logger.info("Testing WordPress utilities...")
    
    results = {
        'success': True,
        'tests': {}
    }
    
    # Test cache
    try:
        cache = WordPressCache(ttl_seconds=10)
        cache.set('test_key', 'test_value')
        value = cache.get('test_key')
        
        results['tests']['cache'] = {
            'success': value == 'test_value',
            'message': f"Cache test {'successful' if value == 'test_value' else 'failed'}"
        }
        
        # Test expiration
        time.sleep(11)  # Wait for cache to expire
        value = cache.get('test_key')
        
        results['tests']['cache_expiration'] = {
            'success': value is None,
            'message': f"Cache expiration test {'successful' if value is None else 'failed'}"
        }
        
        cache.clear()
    except Exception as e:
        results['tests']['cache'] = {
            'success': False,
            'message': f"Cache test failed: {e}"
        }
        results['success'] = False
        
    # Test content optimization
    try:
        test_content = "This is a test paragraph.\n\nThis is another paragraph."
        optimized = WordPressContentTools.optimize_html_content(test_content)
        
        results['tests']['content_optimization'] = {
            'success': '<p>' in optimized,
            'message': f"Content optimization {'successful' if '<p>' in optimized else 'failed'}"
        }
        
        # Test image extraction
        img_content = '<img src="https://example.com/image.jpg"> <img src="https://example.com/image2.png">'
        images = WordPressContentTools.extract_images_from_content(img_content)
        
        results['tests']['image_extraction'] = {
            'success': len(images) == 2,
            'message': f"Image extraction found {len(images)} images"
        }
        
        # Test slug generation
        test_title = "This is a Test Title! With Special Characters?"
        slug = WordPressContentTools.generate_slug(test_title)
        
        results['tests']['slug_generation'] = {
            'success': slug == 'this-is-a-test-title-with-special-characters',
            'message': f"Generated slug: {slug}"
        }
    except Exception as e:
        results['tests']['content_processing'] = {
            'success': False,
            'message': f"Content processing tests failed: {e}"
        }
        results['success'] = False
        
    logger.info(f"WordPress utilities tests completed: {results['success']}")
    return results
