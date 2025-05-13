"""
News Fetcher - A module for retrieving news data from various sources.
Supports RSS feeds, news APIs, and direct web scraping.
"""
import os
import logging
import json
import requests
import feedparser
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from time import mktime
from pathlib import Path

logger = logging.getLogger("TEC.NewsFetcher")

class NewsFetcher:
    """
    Handles retrieval of news data from various sources.
    Supports RSS feeds, news APIs, and direct web scraping.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the NewsFetcher with configuration.
        
        Args:
            config_path: Path to configuration file or directory
        """
        self.sources = []
        self.api_keys = {}
        self.cache_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'news_cache')
        self.cache_expiry = 3600  # Default cache expiry in seconds (1 hour)
        
        # Ensure cache directory exists
        os.makedirs(self.cache_dir, exist_ok=True)
        
        # Load configuration if provided
        if config_path:
            self._load_config(config_path)
        else:
            # Try to load from default location
            default_config = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'config', 'news_sources.json')
            if os.path.exists(default_config):
                self._load_config(default_config)
            else:
                logger.warning("No news sources configuration found. Using default sources.")
                self._load_default_sources()

        # Load API keys from environment variables
        self._load_api_keys()

    def _load_config(self, config_path: str):
        """Load news sources configuration from file."""
        try:
            if os.path.isdir(config_path):
                config_path = os.path.join(config_path, 'news_sources.json')
                
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    config = json.load(f)
                
                self.sources = config.get('sources', [])
                self.cache_expiry = config.get('cache_expiry', 3600)
                
                logger.info(f"Loaded {len(self.sources)} news sources from configuration")
            else:
                logger.warning(f"Config file not found at {config_path}. Using default sources.")
                self._load_default_sources()
        except Exception as e:
            logger.error(f"Error loading news sources configuration: {e}")
            self._load_default_sources()

    def _load_default_sources(self):
        """Load a default set of news sources."""
        self.sources = [
            {
                "name": "Hacker News",
                "url": "https://news.ycombinator.com/rss",
                "type": "rss",
                "category": "technology"
            },
            {
                "name": "TechCrunch",
                "url": "https://techcrunch.com/feed/",
                "type": "rss",
                "category": "technology"
            },
            {
                "name": "MIT Technology Review",
                "url": "https://www.technologyreview.com/feed/",
                "type": "rss",
                "category": "technology"
            },
            {
                "name": "Wired",
                "url": "https://www.wired.com/feed/rss",
                "type": "rss",
                "category": "technology"
            },
            {
                "name": "The Verge",
                "url": "https://www.theverge.com/rss/index.xml",
                "type": "rss",
                "category": "technology"
            }
        ]
        logger.info("Loaded default news sources")

    def _load_api_keys(self):
        """Load API keys from environment variables."""
        # NewsAPI
        news_api_key = os.getenv("NEWS_API_KEY")
        if news_api_key:
            self.api_keys["news_api"] = news_api_key
            
        # GDELT API
        gdelt_api_key = os.getenv("GDELT_API_KEY")
        if gdelt_api_key:
            self.api_keys["gdelt"] = gdelt_api_key
            
        # Add more API keys as needed

    def fetch_all_sources(self, max_age_days: int = 1) -> List[Dict[str, Any]]:
        """
        Fetch articles from all configured sources.
        
        Args:
            max_age_days: Maximum age of articles to fetch in days
            
        Returns:
            List of articles from all sources
        """
        all_articles = []
        
        for source in self.sources:
            try:
                source_type = source.get("type", "rss")
                
                if source_type == "rss":
                    articles = self._fetch_rss(source)
                elif source_type == "news_api":
                    articles = self._fetch_news_api(source)
                elif source_type == "web":
                    articles = self._fetch_web_scrape(source)
                else:
                    logger.warning(f"Unknown source type: {source_type}")
                    continue
                
                # Filter by age
                cutoff_date = datetime.now() - timedelta(days=max_age_days)
                filtered_articles = []
                
                for article in articles:
                    publish_date = article.get("published_datetime")
                    if publish_date and publish_date >= cutoff_date:
                        filtered_articles.append(article)
                
                all_articles.extend(filtered_articles)
                
                logger.info(f"Fetched {len(filtered_articles)} recent articles from {source['name']}")
                
            except Exception as e:
                logger.error(f"Error fetching from {source.get('name', 'unknown')}: {e}")
        
        # Sort by publication date, newest first
        all_articles.sort(key=lambda x: x.get("published_datetime", datetime.min), reverse=True)
        
        return all_articles

    def _fetch_rss(self, source: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Fetch articles from an RSS feed.
        
        Args:
            source: Source configuration dictionary
            
        Returns:
            List of articles from the RSS feed
        """
        cache_file = self._get_cache_file(source)
        
        # Check if cached data is available and recent
        cached_data = self._check_cache(cache_file)
        if cached_data:
            return cached_data
        
        try:
            feed = feedparser.parse(source["url"])
            articles = []
            
            for entry in feed.entries:
                # Extract the publication date
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    published_datetime = datetime.fromtimestamp(mktime(entry.published_parsed))
                else:
                    published_datetime = datetime.now()
                
                # Extract content
                content = ""
                if hasattr(entry, 'content'):
                    for content_item in entry.content:
                        content += content_item.value
                elif hasattr(entry, 'summary'):
                    content = entry.summary
                
                # Clean HTML if present
                if content:
                    soup = BeautifulSoup(content, 'html.parser')
                    content = soup.get_text()
                
                article = {
                    "title": entry.title,
                    "url": entry.link,
                    "source": source["name"],
                    "category": source.get("category", "general"),
                    "published": entry.get("published", ""),
                    "published_datetime": published_datetime,
                    "summary": content,
                    "content": content
                }
                
                articles.append(article)
            
            # Cache the results
            self._cache_results(cache_file, articles)
            
            return articles
            
        except Exception as e:
            logger.error(f"Error fetching RSS feed {source['url']}: {e}")
            return []

    def _fetch_news_api(self, source: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Fetch articles from NewsAPI.
        
        Args:
            source: Source configuration dictionary
            
        Returns:
            List of articles from the NewsAPI
        """
        if "news_api" not in self.api_keys:
            logger.error("News API key not configured")
            return []
        
        cache_file = self._get_cache_file(source)
        
        # Check if cached data is available and recent
        cached_data = self._check_cache(cache_file)
        if cached_data:
            return cached_data
        
        try:
            url = "https://newsapi.org/v2/top-headlines"
            
            # Prepare query parameters
            params = {
                "apiKey": self.api_keys["news_api"],
                "category": source.get("category", "technology"),
                "language": source.get("language", "en"),
                "pageSize": source.get("page_size", 100)
            }
            
            # Add optional country parameter if specified
            if "country" in source:
                params["country"] = source["country"]
                
            # Add optional sources parameter if specified
            if "sources" in source:
                params["sources"] = source["sources"]
            
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                articles = []
                
                for article_data in data.get("articles", []):
                    # Parse the publication date
                    published_datetime = None
                    if article_data.get("publishedAt"):
                        try:
                            published_datetime = datetime.fromisoformat(article_data["publishedAt"].replace("Z", "+00:00"))
                        except:
                            published_datetime = datetime.now()
                    
                    article = {
                        "title": article_data.get("title", ""),
                        "url": article_data.get("url", ""),
                        "source": article_data.get("source", {}).get("name", source["name"]),
                        "category": source.get("category", "general"),
                        "published": article_data.get("publishedAt", ""),
                        "published_datetime": published_datetime,
                        "summary": article_data.get("description", ""),
                        "content": article_data.get("content", "")
                    }
                    
                    articles.append(article)
                
                # Cache the results
                self._cache_results(cache_file, articles)
                
                return articles
            else:
                logger.error(f"News API error: {response.status_code} - {response.text}")
                return []
                
        except Exception as e:
            logger.error(f"Error fetching from News API: {e}")
            return []

    def _fetch_web_scrape(self, source: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Fetch articles by web scraping.
        
        Args:
            source: Source configuration dictionary
            
        Returns:
            List of articles from web scraping
        """
        # This is a simplified implementation
        # For production use, you'd want to implement specific scrapers for each site
        cache_file = self._get_cache_file(source)
        
        # Check if cached data is available and recent
        cached_data = self._check_cache(cache_file)
        if cached_data:
            return cached_data
            
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(source["url"], headers=headers)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # This is a very simplified scraping approach
                # You would need to customize this for each website
                articles = []
                
                # Look for articles based on common patterns
                article_elements = soup.select(source.get("article_selector", "article"))
                
                for element in article_elements:
                    # Try to extract title, link, etc.
                    title_element = element.select_one(source.get("title_selector", "h2, h3, h1"))
                    link_element = element.select_one(source.get("link_selector", "a"))
                    summary_element = element.select_one(source.get("summary_selector", "p"))
                    
                    if title_element and link_element:
                        title = title_element.get_text().strip()
                        link = link_element.get("href", "")
                        
                        # Handle relative URLs
                        if link.startswith("/"):
                            base_url = "/".join(source["url"].split("/")[:3])  # http(s)://domain.com
                            link = base_url + link
                        
                        summary = ""
                        if summary_element:
                            summary = summary_element.get_text().strip()
                        
                        article = {
                            "title": title,
                            "url": link,
                            "source": source["name"],
                            "category": source.get("category", "general"),
                            "published": "",  # Often difficult to extract consistently
                            "published_datetime": datetime.now(),  # Default to current time
                            "summary": summary,
                            "content": summary
                        }
                        
                        articles.append(article)
                
                # Cache the results
                self._cache_results(cache_file, articles)
                
                return articles
            else:
                logger.error(f"Error scraping {source['url']}: HTTP {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Error scraping {source['url']}: {e}")
            return []

    def _get_cache_file(self, source: Dict[str, Any]) -> str:
        """Get the cache file path for a source."""
        source_name = source["name"].lower().replace(" ", "_")
        return os.path.join(self.cache_dir, f"{source_name}.json")

    def _check_cache(self, cache_file: str) -> List[Dict[str, Any]]:
        """
        Check if cache file exists and is recent enough.
        
        Args:
            cache_file: Path to the cache file
            
        Returns:
            List of cached articles or empty list if cache is invalid
        """
        if not os.path.exists(cache_file):
            return []
            
        # Check if cache is still valid
        cache_time = os.path.getmtime(cache_file)
        now = datetime.now().timestamp()
        
        if now - cache_time > self.cache_expiry:
            return []  # Cache expired
            
        try:
            # Load cache
            with open(cache_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Convert string dates back to datetime objects
            for article in data:
                if "published_datetime" in article and isinstance(article["published_datetime"], str):
                    try:
                        article["published_datetime"] = datetime.fromisoformat(article["published_datetime"])
                    except:
                        article["published_datetime"] = datetime.now()
                
            return data
            
        except Exception as e:
            logger.error(f"Error reading cache file {cache_file}: {e}")
            return []

    def _cache_results(self, cache_file: str, articles: List[Dict[str, Any]]):
        """
        Cache the results to a file.
        
        Args:
            cache_file: Path to the cache file
            articles: List of articles to cache
        """
        try:
            # Convert datetime objects to ISO format strings for JSON serialization
            for article in articles:
                if "published_datetime" in article and isinstance(article["published_datetime"], datetime):
                    article["published_datetime"] = article["published_datetime"].isoformat()
            
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(articles, f, indent=2)
                
        except Exception as e:
            logger.error(f"Error caching results to {cache_file}: {e}")


if __name__ == "__main__":
    # Configure logging for standalone testing
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Test the NewsFetcher
    fetcher = NewsFetcher()
    articles = fetcher.fetch_all_sources()
    
    print(f"Fetched {len(articles)} articles")
    
    # Display the first few articles
    for i, article in enumerate(articles[:5]):
        print(f"\nArticle {i+1}:")
        print(f"Title: {article['title']}")
        print(f"Source: {article['source']}")
        print(f"URL: {article['url']}")
        print(f"Published: {article['published']}")
