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
                categories_from_wp = response.json()
                
                # Update the category IDs - ensuring all fetched categories are added/updated
                for category_wp in categories_from_wp:
                    slug = category_wp.get("slug")
                    if slug: # Ensure slug is not None or empty
                        self.categories[slug] = category_wp.get("id") # Add/update all fetched categories
                
                self.logger.debug(f"Retrieved {len(categories_from_wp)} categories and updated cache. Current cache: {self.categories}")
                return categories_from_wp
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
            
            # Handle categories conversion from strings to IDs if needed
            if 'categories' in post_data and post_data['categories']:
                category_ids = []
                for cat_name_or_slug in post_data['categories']:
                    if isinstance(cat_name_or_slug, int):
                        category_ids.append(cat_name_or_slug)
                        continue
                    
                    cat_id = self.categories.get(cat_name_or_slug)
                    if cat_id is None:
                        self.logger.info(f"Category \'{cat_name_or_slug}\' not in cache. Refreshing categories.")
                        self.get_categories() # Refresh cache
                        cat_id = self.categories.get(cat_name_or_slug)
                            
                    if cat_id:
                        category_ids.append(cat_id)
                        self.logger.debug(f"Converted category \'{cat_name_or_slug}\' to ID {cat_id}")
                    else:
                        self.logger.warning(f"Category \'{cat_name_or_slug}\' not found even after refresh. Make sure it exists in WordPress with the exact slug.")
                
                if category_ids:
                    post_data['categories'] = category_ids
                else:
                    self.logger.warning(f"No valid category IDs found for input: {post_data.get('categories')}. Attempting to use \'uncategorized\'.")
                    uncategorized_id = self.categories.get("uncategorized")
                    if uncategorized_id is None: # Try refreshing if not found in cache
                        self.logger.info("Fallback category \'uncategorized\' not in cache. Refreshing categories.")
                        self.get_categories()
                        uncategorized_id = self.categories.get("uncategorized")

                    if uncategorized_id:
                        post_data['categories'] = [uncategorized_id]
                        self.logger.info(f"Using uncategorized (ID: {uncategorized_id}) as fallback.")
                    else:
                        self.logger.warning("Fallback category \'uncategorized\' also not found or has no ID. Post will be sent without category information or assigned to WordPress default.")
                        if 'categories' in post_data: # It was originally present
                           del post_data['categories'] # Remove it to avoid API error
            
            # Handle tags conversion if needed
            if 'tags' in post_data and post_data['tags']:
                tag_ids = []
                for tag in post_data['tags']:
                    # If it's a string, create or get the tag ID
                    if isinstance(tag, str):
                        tag_id = self._create_or_get_tag(tag)
                        if tag_id:
                            tag_ids.append(tag_id)
                    # If it's already an ID, use it directly
                    elif isinstance(tag, int):
                        tag_ids.append(tag)
                
                if tag_ids:
                    post_data['tags'] = tag_ids
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
                
                if post_id:
                    self.logger.info(f"Created post with ID {post_id}: {post_title}")
                    
                    # Return the response data with success flag
                    response_data["success"] = True
                    return response_data
                else:
                    self.logger.error(f"Failed to create post: {title}")
                    return {"success": False, "error": "Failed to get post ID from response"}
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
    
    def create_category(self, name: str, slug: str = None) -> Optional[int]:
        """
        Create a new category in WordPress if it doesn't exist.
        
        Args:
            name: The category name
            slug: Optional slug (will be auto-generated from name if not provided)
            
        Returns:
            The category ID if successful, None otherwise
        """
        if not self.api_base_url:
            self.logger.error("Cannot create category: API base URL not set")
            return None
            
        slug = slug or name.lower().replace(' ', '-')
        
        # First check if the category already exists
        self.get_categories()
        if slug in self.categories and self.categories[slug]:
            self.logger.info(f"Category '{name}' (slug: {slug}) already exists with ID {self.categories[slug]}")
            return self.categories[slug]
            
        # Create the category
        try:
            url = f"{self.api_base_url}/categories"
            category_data = {
                "name": name,
                "slug": slug
            }
            
            response = self._try_multiple_auth_methods("POST", url, category_data)
            
            if response and response.status_code in [200, 201]:
                category_id = response.json().get("id")
                if category_id:
                    # Update our local cache
                    self.categories[slug] = category_id
                    self.logger.info(f"Created category '{name}' with ID {category_id}")
                    return category_id
                else:
                    self.logger.error(f"Failed to extract category ID from response")
                    return None
            else:
                status_code = response.status_code if response else "No response"
                self.logger.error(f"Failed to create category: Status {status_code}")
                return None
                
        except Exception as e:
            self.logger.error(f"Error creating category: {e}")
            return None
    
    def _create_or_get_tag(self, tag_name: str) -> Optional[int]:
        """
        Create a tag if it doesn't exist or get its ID if it does.
        
        Args:
            tag_name: The tag name
            
        Returns:
            The tag ID if successful, None otherwise
        """
        if not self.api_base_url:
            self.logger.error("Cannot create/get tag: API base URL not set")
            return None
            
        # First check if the tag exists
        try:
            # Create slug from tag name
            tag_slug = tag_name.lower().replace(' ', '-')
            url = f"{self.api_base_url}/tags?slug={tag_slug}"
            response = self._try_multiple_auth_methods("GET", url)
            
            if response and response.status_code == 200:
                tags = response.json()
                if tags and len(tags) > 0:
                    tag_id = tags[0].get("id")
                    self.logger.debug(f"Found existing tag '{tag_name}' with ID {tag_id}")
                    return tag_id
                    
            # If we get here, the tag doesn't exist or we couldn't retrieve it
            # Create it
            url = f"{self.api_base_url}/tags"
            tag_data = {
                "name": tag_name,
                "slug": tag_slug
            }
            
            create_response = self._try_multiple_auth_methods("POST", url, tag_data)
            
            if create_response and create_response.status_code in [200, 201]:
                tag_id = create_response.json().get("id")
                self.logger.debug(f"Created tag '{tag_name}' with ID {tag_id}")
                return tag_id
            else:
                status_code = create_response.status_code if create_response else "No response"
                self.logger.error(f"Failed to create tag: Status {status_code}")
                return None
                
        except Exception as e:
            self.logger.error(f"Error creating/getting tag: {e}")
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
    
    def get_posts(self, search_params: Dict[str, Any] = None, per_page: int = 20) -> List[Dict[str, Any]]:
        """
        Get posts from WordPress with optional search parameters.
        
        Args:
            search_params: Optional dictionary with parameters for filtering posts
                Options include: search, author, category, tag, status
            per_page: Number of posts to return per page (default: 20, max: 100)
            
        Returns:
            List of posts matching the search criteria
        """
        if not self.api_base_url:
            self.logger.error("Cannot fetch posts: API base URL not set")
            return []
            
        # Start with default parameters
        params = {
            "per_page": min(per_page, 100)  # WP API max is 100
        }
        
        # Add any provided search parameters
        if search_params:
            params.update(search_params)
            
        try:
            url = f"{self.api_base_url}/posts"
            
            # Make the request
            response = self._try_multiple_auth_methods("GET", url)
            
            if response and response.status_code == 200:
                posts = response.json()
                self.logger.info(f"Retrieved {len(posts)} posts from WordPress")
                return posts
            else:
                status_code = response.status_code if response else "No response"
                self.logger.error(f"Failed to get posts: Status {status_code}")
                return []
                
        except Exception as e:
            self.logger.error(f"Error retrieving posts: {e}")
            return []
    
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
