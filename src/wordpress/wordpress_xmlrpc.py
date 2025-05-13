"""
WordPress Integration for The Elidoras Codex.
This module provides tools for working with WordPress sites using the XML-RPC API.
"""
import os
import logging
from typing import Dict, Any, List, Optional
import xmlrpc.client
from datetime import datetime

from ..utils.helpers import sanitize_filename, get_timestamp

# Configure logging
logger = logging.getLogger("TEC.WordPress")

class WordPressXMLRPC:
    """
    WordPress XML-RPC client for direct interaction with WordPress sites.
    This is an alternative to the REST API approach used in wp_poster.py.
    """
    
    def __init__(self):
        """
        Initialize the WordPress XML-RPC client.
        Retrieves credentials from environment variables.
        """
        self.site_url = os.getenv("WP_URL")
        self.xmlrpc_path = os.getenv("WP_XMLRPC_PATH", "/xmlrpc.php")
        self.username = os.getenv("WP_USERNAME")
        self.password = os.getenv("WP_PASSWORD")
        
        # Check for required credentials
        if not all([self.site_url, self.username, self.password]):
            logger.error("WordPress credentials not fully configured in environment variables")
            self.client = None
        else:
            # Set up XML-RPC endpoint
            self.xmlrpc_url = f"{self.site_url.rstrip('/')}{self.xmlrpc_path}"
            
            try:
                self.client = xmlrpc.client.ServerProxy(self.xmlrpc_url)
                logger.info(f"WordPress XML-RPC client initialized for {self.site_url}")
            except Exception as e:
                logger.error(f"Failed to initialize WordPress XML-RPC client: {e}")
                self.client = None
    
    def is_connected(self) -> bool:
        """
        Check if the client is connected and credentials are valid.
        
        Returns:
            True if connected, False otherwise
        """
        if not self.client:
            return False
            
        try:
            # Try to get the user info to verify credentials
            user = self.client.wp.getProfile("", self.username, self.password)
            return isinstance(user, dict)
        except Exception as e:
            logger.error(f"WordPress connection test failed: {e}")
            return False
    
    def get_posts(self, num_posts: int = 5) -> List[Dict[str, Any]]:
        """
        Get recent posts from the WordPress site.
        
        Args:
            num_posts: Number of posts to retrieve
            
        Returns:
            List of posts
        """
        if not self.client:
            logger.error("WordPress XML-RPC client not initialized")
            return []
            
        try:
            # Get recent posts
            posts = self.client.wp.getPosts("", self.username, self.password, {
                "number": num_posts,
                "orderby": "post_date",
                "order": "DESC"
            })
            
            logger.info(f"Retrieved {len(posts)} posts from WordPress")
            return posts
        except Exception as e:
            logger.error(f"Failed to get WordPress posts: {e}")
            return []
    
    def create_post(self, title: str, content: str, categories: List[str] = None,
                  tags: List[str] = None, status: str = "draft") -> Dict[str, Any]:
        """
        Create a new post on the WordPress site.
        
        Args:
            title: Post title
            content: Post content
            categories: List of category names
            tags: List of tag names
            status: Publication status (draft, publish, etc.)
            
        Returns:
            Dictionary with post ID and URL if successful
        """
        if not self.client:
            logger.error("WordPress XML-RPC client not initialized")
            return {"success": False, "error": "XML-RPC client not initialized"}
            
        try:
            # Set up post data
            post_data = {
                "post_title": title,
                "post_content": content,
                "post_status": status
            }
            
            # Add categories if provided
            if categories:
                post_data["terms"] = {"category": categories}
                
            # Add tags if provided
            if tags:
                if "terms" not in post_data:
                    post_data["terms"] = {}
                post_data["terms"]["post_tag"] = tags
            
            # Create the post
            post_id = self.client.wp.newPost("", self.username, self.password, post_data)
            
            if post_id:
                logger.info(f"Created WordPress post with ID {post_id}: {title}")
                
                # Construct the URL
                post_url = f"{self.site_url}/?"
                if status == "publish":
                    post_url = f"{self.site_url}/?p={post_id}"
                
                return {
                    "success": True,
                    "post_id": post_id,
                    "title": title,
                    "url": post_url,
                    "status": status
                }
            else:
                logger.error(f"Failed to create WordPress post: {title}")
                return {"success": False, "error": "Failed to create post"}
                
        except Exception as e:
            logger.error(f"Error creating WordPress post: {e}")
            return {"success": False, "error": str(e)}
    
    def upload_media(self, file_path: str, name: Optional[str] = None) -> Dict[str, Any]:
        """
        Upload media to the WordPress site.
        
        Args:
            file_path: Path to the file to upload
            name: Optional name for the media file
            
        Returns:
            Dictionary with media information if successful
        """
        if not self.client:
            logger.error("WordPress XML-RPC client not initialized")
            return {"success": False, "error": "XML-RPC client not initialized"}
            
        if not os.path.exists(file_path):
            logger.error(f"Media file not found: {file_path}")
            return {"success": False, "error": f"File not found: {file_path}"}
            
        try:
            # Use the file name if no name is provided
            if not name:
                name = sanitize_filename(os.path.basename(file_path))
                
            # Read the file data
            with open(file_path, "rb") as f:
                file_data = f.read()
                
            # Create media data structure
            media_data = {
                "name": name,
                "type": _get_mimetype(file_path),
                "bits": xmlrpc.client.Binary(file_data)
            }
            
            # Upload the media
            response = self.client.wp.uploadFile("", self.username, self.password, media_data)
            
            if response and "url" in response:
                logger.info(f"Uploaded media: {name}")
                return {"success": True, "media": response}
            else:
                logger.error(f"Failed to upload media: {name}")
                return {"success": False, "error": "Upload failed"}
                
        except Exception as e:
            logger.error(f"Error uploading media: {e}")
            return {"success": False, "error": str(e)}


def _get_mimetype(file_path: str) -> str:
    """
    Get the MIME type of a file.
    
    Args:
        file_path: Path to the file
        
    Returns:
        MIME type string
    """
    import mimetypes
    
    # Initialize MIME types if not already done
    if not mimetypes.inited:
        mimetypes.init()
        
    # Get MIME type based on file extension
    mime_type, _ = mimetypes.guess_type(file_path)
    
    # Return application/octet-stream if type couldn't be determined
    return mime_type or "application/octet-stream"


def test_wordpress_connection() -> Dict[str, Any]:
    """
    Test the WordPress connection.
    
    Returns:
        Dictionary with connection status and information
    """
    wp = WordPressXMLRPC()
    connected = wp.is_connected()
    
    result = {
        "success": connected,
        "timestamp": get_timestamp(),
        "site_url": wp.site_url if wp.site_url else "Not configured"
    }
    
    if connected:
        # Get some basic site info
        try:
            # Get recent posts as a test
            posts = wp.get_posts(1)
            result["posts_retrieved"] = len(posts) > 0
            result["message"] = "Connection successful"
        except Exception as e:
            result["error"] = str(e)
            result["message"] = "Connection partially successful"
    else:
        result["message"] = "Connection failed"
        
    return result
