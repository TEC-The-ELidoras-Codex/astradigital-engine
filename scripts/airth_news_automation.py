#!/usr/bin/env python3
"""
Airth News Automation System

This script automates the process of:
1. Gathering news from various sources
2. Processing and clustering news into topics
3. Generating SEO-optimized blog articles
4. Publishing articles to WordPress

Can be run manually or scheduled via cron/Task Scheduler.
"""
import os
import sys
import logging
import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
import random
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure logging
log_dir = os.path.join(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__))),
    'logs')
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(
            os.path.join(
                log_dir,
                f"airth_news_automation_{
                    datetime.now().strftime('%Y%m%d')}.log"))])
logger = logging.getLogger("AirthNewsAutomation")

# Import required modules
try:
    from dotenv import load_dotenv
    from src.utils.news_fetcher import NewsFetcher
    from src.utils.news_processor import NewsProcessor
    from src.utils.content_generator import ContentGenerator
    from src.agents.airth_agent import AirthAgent
except ImportError as e:
    logger.critical(f"Failed to import required modules: {e}")
    print(f"Error: Failed to import required modules. Make sure all dependencies are installed.")
    print(f"Details: {e}")
    sys.exit(1)

# Load environment variables
env_path = os.path.join(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__))),
    'config',
    '.env')
load_dotenv(env_path)


class AirthNewsAutomation:
    """
    Orchestrates the automated news gathering, processing, and publishing workflow.
    """

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the automation system.

        Args:
            config_path: Path to configuration directory or file
        """
        self.config_path = config_path or os.path.join(os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))), 'config')

        # Track statistics
        self.stats = {
            "articles_fetched": 0,
            "topics_generated": 0,
            "articles_created": 0,
            "articles_published": 0,
            "errors": 0
        }

        # Initialize components
        logger.info("Initializing Airth News Automation System")

        try:
            # Create an adapter that uses the WordPress posting capabilities
            # without depending on the LLM client
            class AirthWPAdapter:
                """Adapter to provide WordPress functionality."""

                def __init__(self):
                    self.logger = logging.getLogger("AirthWPAdapter")
                    # Import what we need for WordPress posting
                    from src.agents.wp_poster import WordPressAgent

                    # Check if OpenAI is available
                    self.openai_available = False
                    try:
                        import openai
                        from openai import OpenAI
                        self.openai_available = True
                        self.logger.info("OpenAI module loaded successfully")
                    except ImportError as e:
                        self.logger.error(f"OpenAI module not found. Error: {e}")
                        self.openai_available = False

                    # Initialize OpenAI client
                    self.llm_client = None
                    if self.openai_available:
                        try:
                            openai_api_key = os.getenv("OPENAI_API_KEY")
                            if not openai_api_key:
                                self.logger.error("OpenAI API key not found in environment variables.")
                            else:
                                self.llm_client = OpenAI(api_key=openai_api_key)
                                self.logger.info("OpenAI client initialized successfully.")
                        except Exception as e:
                            self.logger.error(f"Failed to initialize OpenAI client: {e}")
                    
                    # Load config from the same place as AirthAgent would
                    config_path = os.path.join(
                        os.path.dirname(
                            os.path.dirname(
                                os.path.abspath(__file__))),
                        'config')
                    self.wp_agent = WordPressAgent(config_path=config_path)
                    self.logger.info(
                        "WordPress Agent initialized directly with config path")

                def _interact_llm(self, prompt, max_tokens=None):
                    """Generate content using OpenAI API."""
                    if not max_tokens:
                        max_tokens = 1000  # Default max tokens
                    
                    if not self.llm_client:
                        self.logger.warning("LLM client not available. Using fallback content generation.")
                        return f"Generated content based on {prompt[:30]}... [OpenAI API not available]"
                    
                    try:
                        # Using similar parameters to AirthAgent implementation
                        response = self.llm_client.completions.create(
                            model="gpt-3.5-turbo-instruct",  # Using a standard model
                            prompt=prompt,
                            max_tokens=max_tokens,
                            n=1,
                            stop=None,
                            temperature=0.7,
                        )
                        
                        self.logger.info(f"OpenAI API call successful, generated content of length: {len(response.choices[0].text)}")
                        return response.choices[0].text.strip()
                    except Exception as e:
                        self.logger.error(f"OpenAI API call failed: {e}")
                        return f"Error: OpenAI API call failed: {e}"

                def post_to_wordpress(
                        self,
                        title,
                        content,
                        category="technology_ai",
                        tags=None,
                        status="draft"):
                    """Direct WordPress posting through wp_agent."""
                    if not self.wp_agent:
                        logger.error("WordPress agent not initialized")
                        return {"success": False,
                                "error": "WordPress agent not initialized"}

                    logger.info(f"Posting article to WordPress: {title}")

                    try:
                        # Create a post data dictionary to match the expected format
                        # Important: For categories, we pass the slug name as a string, and wp_agent.create_post 
                        # will handle the conversion to category ID internally
                        post_data = {
                            'title': title,
                            'content': content,
                            'status': status
                        }
                        
                        # Pass category as a separate parameter to let create_post handle ID lookup
                        if category:
                            # The category is passed as a separate parameter now, not in the dict
                            pass
                            
                        # Handle tags
                        if tags:
                            post_data['tags'] = tags

                        # Pass the dictionary and category separately to allow category ID lookup
                        result = self.wp_agent.create_post(post_data, category=category)

                        # Format the result to match expected structure
                        return {
                            "success": result.get("success", False), 
                            "post_id": result.get("id", "0"), 
                            "url": result.get("link", ""), 
                            "error": None if result.get("success", False) else "Failed to create post"
                        }
                    except Exception as e:
                        logger.error(f"Error posting to WordPress: {e}")
                        return {"success": False, "error": str(e)}
                
                def check_for_duplicate_article(self, title, content=None, similarity_threshold=0.8):
                    """
                    Check if a similar article already exists in WordPress.
                    
                    Args:
                        title: Title of the new article
                        content: Optional content of the new article
                        similarity_threshold: Threshold for title similarity (0.0 to 1.0)
                        
                    Returns:
                        Tuple (is_duplicate, existing_post_info) where:
                        - is_duplicate: Boolean indicating if a duplicate was found
                        - existing_post_info: Dict with info about the matching post if found, None otherwise
                    """
                    if not self.wp_agent:
                        logger.error("WordPress agent not initialized")
                        return False, None
                    
                    try:
                        # Get recent posts from WordPress
                        existing_posts = self.wp_agent.get_posts(per_page=50)
                        
                        if not existing_posts:
                            logger.info("No existing posts found in WordPress")
                            return False, None
                        
                        # Normalize the new title for comparison (lowercase, strip punctuation)
                        import re
                        from difflib import SequenceMatcher
                        
                        def normalize_title(title_text):
                            # Convert to lowercase, remove punctuation, and extra spaces
                            return re.sub(r'[^\w\s]', '', title_text.lower()).strip()
                        
                        def calculate_similarity(text1, text2):
                            # Use SequenceMatcher to calculate similarity between strings
                            return SequenceMatcher(None, text1, text2).ratio()
                        
                        normalized_new_title = normalize_title(title)
                        
                        # Check each existing post for similarity
                        for post in existing_posts:
                            existing_title = post.get("title", {}).get("rendered", "")
                            if not existing_title:
                                continue
                                
                            # Compare normalized titles
                            normalized_existing_title = normalize_title(existing_title)
                            similarity = calculate_similarity(normalized_new_title, normalized_existing_title)
                            
                            # If similarity exceeds threshold, consider it a duplicate
                            if similarity > similarity_threshold:
                                logger.info(f"Duplicate article found: '{existing_title}' (similarity: {similarity:.2f})")
                                return True, {
                                    "id": post.get("id"),
                                    "title": existing_title,
                                    "link": post.get("link"),
                                    "similarity": similarity
                                }
                        
                        logger.info("No duplicate articles found")
                        return False, None
                        
                    except Exception as e:
                        logger.error(f"Error checking for duplicate articles: {e}")
                        # If there's an error in checking, default to allowing the post
                        return False, None

            # Use our adapter with WordPress capabilities
            self.airth = AirthWPAdapter()
            logger.info(
                "Created AirthWPAdapter with WordPress publishing capabilities")            # Ensure proper LLM client status is tracked for compatibility
            # No need to set a dummy value since we have a real client now

            # Initialize news fetcher
            self.news_fetcher = NewsFetcher(self.config_path)
            logger.info("News fetcher initialized successfully")

            # Initialize news processor
            self.news_processor = NewsProcessor(self.config_path)
            logger.info("News processor initialized successfully")

            # Initialize content generator with reference to Airth
            self.content_generator = ContentGenerator(
                self.config_path, self.airth)
            logger.info("Content generator initialized successfully")

        except Exception as e:
            logger.critical(f"Failed to initialize components: {e}")
            raise RuntimeError(
                f"Failed to initialize news automation system: {e}")

    def run(self,
            max_age_days: int = 1,
            max_topics: int = 3,
            publish_status: str = "draft",
            enable_publishing: bool = True) -> Dict[str, Any]:
        """
        Run the full automation workflow.

        Args:
            max_age_days: Maximum age in days for news articles to process
            max_topics: Maximum number of topics to process
            publish_status: WordPress publication status ('draft' or 'publish')
            enable_publishing: Whether to publish articles to WordPress

        Returns:
            Statistics about the run
        """
        start_time = time.time()

        logger.info(f"Starting Airth News Automation workflow")
        logger.info(
            f"Parameters: max_age_days={max_age_days}, max_topics={max_topics}, " +
            f"publish_status={publish_status}, enable_publishing={enable_publishing}")

        try:
            # Step 1: Fetch news articles
            logger.info("Step 1: Fetching news articles")
            articles = self.news_fetcher.fetch_all_sources(
                max_age_days=max_age_days)
            self.stats["articles_fetched"] = len(articles)
            logger.info(f"Fetched {len(articles)} news articles")

            if not articles:
                logger.warning("No articles fetched. Exiting workflow.")
                return self.stats

            # Step 2: Process articles into topics
            logger.info("Step 2: Processing articles into topics")
            topics = self.news_processor.process_articles(articles)
            self.stats["topics_generated"] = len(topics)
            logger.info(f"Generated {len(topics)} topic clusters")

            if not topics:
                logger.warning("No topics generated. Exiting workflow.")
                return self.stats

            # Limit to top N topics
            topics = topics[:max_topics]
            logger.info(
                f"Selected top {
                    len(topics)} topics for content generation")

            # Step 3: Generate content for each topic
            logger.info("Step 3: Generating article content")
            generated_articles = []

            for topic in topics:
                logger.info(
                    f"Generating article for topic: {
                        topic.get(
                            'suggested_title',
                            'Topic ' + str(
                                topic.get(
                                    'id',
                                    0)))}")
                try:
                    result = self.content_generator.generate_article_from_topic(
                        topic)

                    if result.get("success"):
                        generated_articles.append(result)
                        logger.info(
                            f"Successfully generated article: {
                                result.get('title')}")
                    else:
                        logger.error(
                            f"Failed to generate article: {
                                result.get('error')}")
                        self.stats["errors"] += 1
                except Exception as e:
                    logger.error(f"Error generating article content: {e}")
                    self.stats["errors"] += 1

            self.stats["articles_created"] = len(generated_articles)
            logger.info(
                f"Generated {
                    len(generated_articles)} articles from topics")

            # Step 4: Publish content to WordPress
            if generated_articles and enable_publishing:
                # Check if Airth has WordPress posting capability
                if hasattr(
                        self.airth,
                        'post_to_wordpress') and hasattr(
                        self.airth,
                        'wp_agent') and self.airth.wp_agent is not None:
                    logger.info(
                        f"Step 4: Publishing articles to WordPress (status: {publish_status})")

                    for article in generated_articles:
                        try:
                            title = article.get("title", "")
                            content = article.get("content", "")
                            category = article.get("category", "technology_ai")
                            tags = article.get("keywords", [])

                            if not title or not content:
                                logger.error(
                                    "Cannot publish article: missing title or content")
                                self.stats["errors"] += 1
                                continue                            # Check for duplicates before publishing
                            is_duplicate, existing_post_info = self.airth.check_for_duplicate_article(
                                title=title,
                                content=content,
                                similarity_threshold=0.7)  # Adjust threshold for more strict duplicate detection

                            if is_duplicate:
                                # Track skipped duplicates in their own stat counter
                                if "duplicates_skipped" not in self.stats:
                                    self.stats["duplicates_skipped"] = 0
                                self.stats["duplicates_skipped"] += 1
                                
                                # Provide detailed log with similarity score
                                similarity = existing_post_info.get('similarity', 0)
                                logger.warning(
                                    f"DUPLICATE DETECTED: '{title}' matches existing post: '{existing_post_info.get('title')}' "
                                    f"(similarity: {similarity:.2%}). Skipping publication.")
                                continue

                            # Publish to WordPress
                            logger.info(f"Publishing article: {title}")
                            result = self.airth.post_to_wordpress(
                                title=title,
                                content=content,
                                category=category,
                                tags=tags,
                                status=publish_status
                            )

                            if result.get("success"):
                                self.stats["articles_published"] += 1
                                logger.info(
                                    f"Article published successfully: {result.get('post_id')} - {result.get('url')}")
                            else:
                                logger.error(
                                    f"Failed to publish article: {
                                        result.get('error')}")
                                self.stats["errors"] += 1
                        except Exception as e:
                            logger.error(f"Error publishing article: {e}")
                            self.stats["errors"] += 1
                else:
                    logger.warning(
                        "WordPress posting capability not available. Skipping publishing.")            # Calculate runtime and success rate
            end_time = time.time()
            runtime_seconds = end_time - start_time
            success_rate = 0 if self.stats["articles_created"] == 0 else self.stats["articles_published"] / \
                self.stats["articles_created"]

            logger.info(
                f"Automation workflow completed in {
                    runtime_seconds:.2f} seconds")
            logger.info(f"Success rate: {success_rate:.2%}")
            
            # Add information about duplicates to the log summary
            duplicates_skipped = self.stats.get("duplicates_skipped", 0)
            if duplicates_skipped > 0:
                logger.info(f"Duplicate articles skipped: {duplicates_skipped}")
                
            logger.info(f"Stats: {json.dumps(self.stats, indent=2)}")

            return self.stats

        except Exception as e:
            logger.error(f"Error in automation workflow: {e}")
            self.stats["errors"] += 1
            return self.stats

    def send_notification(self,
                          success: bool,
                          run_stats: Dict[str,
                                          Any],
                          error_message: Optional[str] = None):
        """Send an email notification about the automation run."""
        try:
            # Check if SMTP settings are available
            smtp_host = os.environ.get("SMTP_HOST")
            smtp_port = os.environ.get("SMTP_PORT")
            smtp_user = os.environ.get("SMTP_USER")
            smtp_pass = os.environ.get("SMTP_PASSWORD")
            recipient = os.environ.get("NOTIFICATION_EMAIL")

            if not all([smtp_host,
                        smtp_port,
                        smtp_user,
                        smtp_pass,
                        recipient]):
                logger.warning(
                    "SMTP settings not configured. Skipping notification.")
                return

            # Create the email message
            msg = MIMEMultipart()
            msg['Subject'] = f"Airth News Automation {
                'Succeeded' if success else 'Failed'}"
            msg['From'] = smtp_user
            msg['To'] = recipient

            # Build the email body
            body_parts = [
                f"Airth News Automation Run: {
                    'Success' if success else 'Failure'}",
                f"Timestamp: {
                    datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                "",
                "Statistics:",
                f"  Articles fetched: {
                    run_stats.get(
                        'articles_fetched',
                        0)}",
                f"  Topics generated: {
                    run_stats.get(
                        'topics_generated',
                        0)}",
                f"  Articles created: {
                    run_stats.get(
                        'articles_created',
                        0)}",                f"  Articles published: {
                    run_stats.get(
                        'articles_published',
                        0)}",
                f"  Duplicates skipped: {
                    run_stats.get(
                        'duplicates_skipped',
                        0)}",
                f"  Errors: {
                    run_stats.get(
                        'errors',
                        0)}",
                "",
            ]

            if error_message:
                body_parts.extend([
                    "Error details:",
                    error_message
                ])

            msg.attach(MIMEText("\n".join(body_parts), 'plain'))

            # Send the email
            with smtplib.SMTP(smtp_host, int(smtp_port)) as server:
                server.starttls()
                server.login(smtp_user, smtp_pass)
                server.send_message(msg)

            logger.info(f"Notification email sent to {recipient}")

        except Exception as e:
            logger.error(f"Failed to send notification: {e}")

    def __str__(self) -> str:
        """String representation of the automation system."""
        return f"AirthNewsAutomation(articles_fetched={
            self.stats['articles_fetched']}, " + f"articles_published={
            self.stats['articles_published']}, " + f"errors={
            self.stats['errors']})"


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Airth News Automation System")
    parser.add_argument(
        "--max-age",
        type=int,
        default=1,
        help="Maximum age of news articles in days")
    parser.add_argument(
        "--max-topics",
        type=int,
        default=3,
        help="Maximum number of topics to process")
    parser.add_argument(
        "--status",
        choices=[
            "draft",
            "publish"],
        default="draft",
        help="Publication status")
    parser.add_argument(
        "--no-publish",
        action="store_true",
        help="Skip publishing to WordPress")
    parser.add_argument(
        "--notify",
        action="store_true",
        help="Send email notification after run")
    parser.add_argument(
        "--config",
        type=str,
        help="Path to configuration directory")

    args = parser.parse_args()

    try:
        # Initialize the automation system
        print(f"\nInitializing Airth News Automation System...")
        automation = AirthNewsAutomation(config_path=args.config)

        # Run the automation
        print(f"Running automation workflow...")
        stats = automation.run(
            max_age_days=args.max_age,
            max_topics=args.max_topics,
            publish_status=args.status,
            enable_publishing=not args.no_publish
        )        # Display summary
        print(f"\nAutomation run completed:")
        print(f"- Articles fetched: {stats['articles_fetched']}")
        print(f"- Topics generated: {stats['topics_generated']}")
        print(f"- Articles created: {stats['articles_created']}")
        print(f"- Articles published: {stats['articles_published']}")
        # Display duplicate information if any duplicates were detected
        if "duplicates_skipped" in stats and stats["duplicates_skipped"] > 0:
            print(f"- Duplicates skipped: {stats['duplicates_skipped']}")
        print(f"- Errors: {stats['errors']}")

        # Send notification if requested
        if args.notify:
            automation.send_notification(
                success=stats["errors"] == 0,
                run_stats=stats,
                error_message=None if stats["errors"] == 0 else "Errors occurred during the automation run"
            )

        # Return success if no errors, otherwise failure
        return 0 if stats["errors"] == 0 else 1

    except Exception as e:
        logger.critical(f"Unhandled exception in main: {e}")
        print(f"\nError: {str(e)}")

        # Send failure notification if requested
        if 'automation' in locals() and args.notify:
            automation.send_notification(
                success=False,
                run_stats=getattr(automation, 'stats', {"errors": 1}),
                error_message=str(e)
            )

        return 1


if __name__ == "__main__":
    sys.exit(main())
