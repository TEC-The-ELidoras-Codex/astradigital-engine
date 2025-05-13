"""
WordPress Posting Agent for The Elidoras Codex.
Handles interactions with WordPress for publishing content.
"""
import os
import logging
import json
import requests
from typing import Dict, Any, List, Optional, Union
from base64 import b64encode

from .base_agent import BaseAgent

class WordPressAgent(BaseAgent):
    """
    WordPressAgent handles interactions with the WordPress API.
    It creates posts, updates content, and manages media uploads.
    """
    
    def __init__(self, config_path: Optional[str] = None, agent_config: Optional[Dict[str, Any]] = None):
        if agent_config is None:
            # Standard initialization if instantiated as a standalone agent
            super().__init__("WordPressAgent", config_path)
            self.logger.info("WordPressAgent initialized as a standalone agent.")
            config_to_use = self.config
        else:
            # Initialization if an already loaded config is passed (e.g., by another agent)
            # We need a name for the logger.
            self.name = "WordPressAgent" # Or make it configurable
            self.logger = logging.getLogger(f"TEC.{self.name}")
            self.config = agent_config
            # Manually load .env variables if not already done by a BaseAgent upstream
            # This path assumes wp_poster.py is in src/agents/
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            env_path = os.path.join(project_root, 'config', '.env')
            if not os.getenv("WP_SITE_URL"): # Check if .env might not have been loaded
                 from dotenv import load_dotenv
                 load_dotenv(env_path, override=True) # Ensure .env are available for os.getenv fallbacks
            self.logger.info("WordPressAgent initialized with provided configuration.")
            config_to_use = self.config        # Initialize WordPress API credentials from the effective configuration
        wp_settings = config_to_use.get("wordpress", {})

        self.wp_site_url = wp_settings.get("site_url", os.getenv("WP_SITE_URL")) or \
                           wp_settings.get("url", os.getenv("WP_URL")) # Supporting "url" for backward compatibility
        self.wp_user = wp_settings.get("user", os.getenv("WP_USER")) or \
                       wp_settings.get("username", os.getenv("WP_USERNAME")) # Supporting "username"
        self.wp_app_pass = wp_settings.get("app_pass", os.getenv("WP_APP_PASS")) or \
                           wp_settings.get("password", os.getenv("WP_PASSWORD")) # Supporting "password"
        self.wp_api_version = wp_settings.get("api_version", os.getenv("WP_API_VERSION", "wp/v2"))

        # Fallback to a default URL if nothing is configured (though this should be rare)
        if not self.wp_site_url:
            self.wp_site_url = "https://elidorascodex.com" # Default as a last resort
            self.logger.warning(f"WordPress site URL not found in config or environment. Using default: {self.wp_site_url}")
        
        if not self.wp_user or not self.wp_app_pass:
            self.logger.warning(
                "WordPress user or application password not fully configured. "
                "Please check your config.yaml, agent-specific JSON, or .env file."
            )
        
        # Process URL to ensure it's properly formatted for the REST API
        # If URL ends with xmlrpc.php, convert it to the base URL
        if self.wp_site_url and self.wp_site_url.endswith('xmlrpc.php'):
            self.wp_site_url = self.wp_site_url.replace('xmlrpc.php', '')
            self.logger.info(f"Converted XML-RPC URL to base URL: {self.wp_site_url}")
        
        # Normalize URL format
        if self.wp_site_url:
            # Remove trailing slash if present
            self.wp_site_url = self.wp_site_url.rstrip('/')
            
            # Build the REST API base URL
            # Check if wp-json is already in the URL
            if '/wp-json' not in self.wp_site_url:
                self.api_base_url = f"{self.wp_site_url}/wp-json/{self.wp_api_version}"
            else:
                # URL already includes wp-json, just add the API version if needed
                if self.wp_site_url.endswith('/wp-json'):
                    self.api_base_url = f"{self.wp_site_url}/{self.wp_api_version}"
                else:
                    # URL has something after wp-json, assume it's the full path
                    self.api_base_url = self.wp_site_url
            
            self.logger.info(f"Using WordPress REST API URL: {self.api_base_url}")
        else:
            self.api_base_url = None
        
        # Predefined categories and tags for TEC content
        self.categories = {
            "airths_codex": None,  # Will be populated during get_categories
            "technology_ai": None,
            "reviews_deepdives": None,
            "uncategorized": None
        }
        
        # Common tags for AI content
        self.common_ai_tags = [
            "ai-ethics", "ai-storytelling", "ai-assisted-writing", 
            "ai-driven-creativity", "ai-generated-content", "ai-human-collaboration",
            "creative-ai-tools"
        ]
        
        # Cache categories on initialization
        if self.api_base_url:
            self.get_categories()
    
    def _get_auth_header(self) -> Dict[str, str]:
        """
        Get the authorization header for WordPress API requests.
        Uses Basic Authentication that works with WordPress.com sites.
        
        Returns:
            Dictionary containing the Authorization header
        """
        if not self.wp_user or not self.wp_app_pass:
            self.logger.error("Cannot create auth header: WordPress credentials not configured")
            return {}
            
        # Convert username to lowercase for consistency
        username = self.wp_user.lower()
        
        # Use Basic Authentication with username and password with spaces
        credentials = f"{username}:{self.wp_app_pass}"
        token = b64encode(credentials.encode()).decode()
        
        self.logger.debug(f"Generated Basic Auth token for WordPress API")
        return {"Authorization": f"Basic {token}"}
    
    def _try_multiple_auth_methods(self, method: str, url: str, data: Dict = None) -> requests.Response:
        """
        Try multiple authentication methods for WordPress API.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            url: API URL to request
            data: Data to send (for POST/PUT)
            
        Returns:
            Response from the successful authentication method or the last attempted response
        """
        # Authentication methods to try in order
        auth_methods = [
            {
                "name": "Bearer token",
                "headers": {
                    **self._get_auth_header(),
                    "Content-Type": "application/json"
                }
            },
            {
                "name": "Basic auth with spaces",
                "auth": (self.wp_user.lower(), self.wp_app_pass)
            }
        ]
        
        last_response = None
        errors = []
        
        # Try each authentication method
        for auth_method in auth_methods:
            try:
                self.logger.debug(f"Trying {auth_method['name']} authentication")
                
                if "headers" in auth_method:
                    # Use headers authentication
                    response = requests.request(
                        method=method,
                        url=url,
                        headers=auth_method["headers"],
                        json=data
                    )
                else:
                    # Use basic auth
                    response = requests.request(
                        method=method,
                        url=url,
                        auth=auth_method["auth"],
                        json=data,
                        headers={"Content-Type": "application/json"}
                    )
                
                last_response = response
                
                # If successful, return the response
                if response.status_code < 400:
                    self.logger.debug(f"Authentication successful with {auth_method['name']}")
                    return response
                else:
                    error = f"{auth_method['name']} failed with status {response.status_code}: {response.text}"
                    self.logger.debug(error)
                    errors.append(error)
                    
            except Exception as e:
                error = f"{auth_method['name']} failed with exception: {e}"
                self.logger.debug(error)
                errors.append(error)
        
        # If all methods failed, log the errors
        self.logger.error(f"All authentication methods failed: {errors}")
        return last_response
    
    def get_categories(self) -> List[Dict[str, Any]]:
        """
        Get the categories from WordPress.
        Populates the self.categories dictionary with category IDs.
        
        Returns:
            List of categories from the WordPress site
        """
        if not self.api_base_url:
            self.logger.error("Cannot get categories: API base URL not set")
            return []
        
        try:
            url = f"{self.api_base_url}/categories"
            response = self._try_multiple_auth_methods("GET", url)
            
            if response and response.status_code == 200:
                categories = response.json()
                
                # Update the category IDs
                for category in categories:
                    slug = category.get("slug")
                    if slug in self.categories:
                        self.categories[slug] = category.get("id")
                
                self.logger.debug(f"Retrieved {len(categories)} categories")
                return categories
            else:
                status_code = response.status_code if response else "No response"
                self.logger.error(f"Failed to get categories: Status {status_code}")
                return []
                
        except Exception as e:
            self.logger.error(f"Error retrieving categories: {e}")
            return []
            
    def create_post(self, title_or_data: Union[str, Dict[str, Any]], content: Optional[str] = None, 
                   category: str = "uncategorized", 
                   tags: List[str] = None,
                   status: str = "draft") -> Dict[str, Any]:
        """
        Create a post on WordPress.
        
        This method supports two calling styles:
        
        Style 1 (separate parameters):
            create_post(title="My Title", content="My Content", status="draft")
            
        Style 2 (dictionary parameter):
            create_post({
                'title': 'My Title', 
                'content': 'My Content',
                'status': 'draft',
                'categories': [1, 2],
                'tags': ['tag1', 'tag2']
            })
        
        Args:
            title_or_data: Either the post title (str) or a dictionary with all post details
            content: The post content HTML (only used if title_or_data is a string)
            category: The category slug to post to (only used if title_or_data is a string)
            tags: The tags to apply to the post (only used if title_or_data is a string)
            status: Publication status (draft, publish, etc.) (only used if title_or_data is a string)
            
        Returns:
            Dictionary with post status and details
        """
        if not self.api_base_url:
            self.logger.error("Cannot create post: API base URL not set")
            return {"success": False, "error": "WordPress API URL not configured"}
            
        if not self.wp_user or not self.wp_app_pass:
            self.logger.error("Cannot create post: WordPress credentials not configured")
            return {"success": False, "error": "WordPress credentials not configured"}
        
        # Handle two different calling styles
        if isinstance(title_or_data, dict):
            # Style 2: Dictionary parameter contains all the post details
            post_data = title_or_data.copy()  # Make a copy to avoid modifying the original
            title = post_data.get('title', '')
        else:
            # Style 1: Separate parameters
            title = title_or_data
            
            # Get category ID
            category_id = self.categories.get(category)
            if category_id is None:
                # Try refreshing categories
                self.get_categories()
                category_id = self.categories.get(category)
                
                # Fall back to uncategorized
                if category_id is None:
                    category_id = self.categories.get("uncategorized")
                    
            # Prepare tag IDs (first create them if they don't exist)
            tag_ids = []
            if tags:
                for tag in tags:
                    tag_id = self._create_or_get_tag(tag)
                    if tag_id:
                        tag_ids.append(tag_id)
            
            # Prepare the post data
            post_data = {
                "title": title,
                "content": content,
                "status": status
            }
            
            # Add categories if available
            if category_id:
                post_data["categories"] = [category_id]
                
            # Add tags if available
            if tag_ids:
                post_data["tags"] = tag_ids
            
        try:            # Create the post
            url = f"{self.api_base_url}/posts"
            response = self._try_multiple_auth_methods("POST", url, post_data)
            
            if response and response.status_code in [200, 201]:
                response_data = response.json()
                post_id = response_data.get("id")
                post_url = response_data.get("link")
                post_status = response_data.get("status", status)
                post_title = response_data.get("title", {}).get("rendered", title)
                
                self.logger.info(f"Created post with ID {post_id}: {post_title}")
                return {
                    "success": True,
                    "post_id": post_id,
                    "title": post_title,
                    "url": post_url,
                    "status": post_status
                }
            else:
                status_code = response.status_code if response else "No response"
                error_message = response.text if response else "No response"
                self.logger.error(f"Failed to create post: Status {status_code}, {error_message}")
                return {
                    "success": False,
                    "error": f"API error: {error_message}",
                    "status_code": status_code
                }
                
        except Exception as e:
            self.logger.error(f"Error creating post: {e}")
            return {"success": False, "error": str(e)}
    
    def _create_or_get_tag(self, tag: str) -> Optional[int]:
        """
        Create a tag if it doesn't exist, or get its ID if it does.
        
        Args:
            tag: The tag name/slug
            
        Returns:
            The tag ID if successful, None otherwise
        """
        if not self.api_base_url:
            self.logger.error("Cannot create tag: API base URL not set")
            return None
            
        try:
            # First check if the tag exists
            search_url = f"{self.api_base_url}/tags?search={tag}"
            search_response = self._try_multiple_auth_methods("GET", search_url)
            
            if search_response and search_response.status_code == 200:
                tags = search_response.json()
                if tags:
                    # Check for exact match
                    for tag_data in tags:
                        if tag_data.get("name").lower() == tag.lower():
                            return tag_data.get("id")
                    
            # Tag doesn't exist, create it
            create_url = f"{self.api_base_url}/tags"
            create_data = {
                "name": tag
            }
            create_response = self._try_multiple_auth_methods("POST", create_url, create_data)
            
            if create_response and create_response.status_code in [200, 201]:
                tag_data = create_response.json()
                return tag_data.get("id")
            else:
                self.logger.error(f"Failed to create tag: {tag}")
                return None
                
        except Exception as e:
            self.logger.error(f"Error working with tag {tag}: {e}")
            return None
    
    def upload_media(self, file_path: str, title: str = None) -> Dict[str, Any]:
        """
        Upload media to WordPress.
        
        Args:
            file_path: Path to the media file
            title: Optional title for the media
            
        Returns:
            Dictionary with media status and details
        """
        # This is a placeholder for media upload functionality
        # WordPress media upload requires a different approach with multipart/form-data
        self.logger.warning("Media upload not yet implemented")
        return {"success": False, "error": "Media upload not implemented"}
    
    def run(self) -> Dict[str, Any]:
        """
        Run a test post to verify WordPress connectivity.
        
        Returns:
            Dictionary with the result of the test
        """
        test_title = "TEC WordPress Connection Test"
        test_content = "<p>This is an automated test post from the WordPressAgent.</p>"
        
        return self.create_post(test_title, test_content, status="draft")


# For testing the agent standalone
if __name__ == "__main__":
    wp_agent = WordPressAgent()
    result = wp_agent.run()
    print(json.dumps(result, indent=2))
