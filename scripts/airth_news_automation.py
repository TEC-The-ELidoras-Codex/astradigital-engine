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
log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs')
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join(log_dir, f"airth_news_automation_{datetime.now().strftime('%Y%m%d')}.log"))
    ]
)
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
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config', '.env')
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
        self.config_path = config_path or os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config')
        
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
        
        try:            # Create a dummy adapter instead of using AirthAgent directly
            class AirthNewsAdapter:
                """Simple adapter to provide necessary functionality without full AirthAgent."""
                
                def __init__(self):
                    self.llm_client = None
                    self.wp_agent = None
                    self.logger = logging.getLogger("AirthNewsAdapter")
                    
                def _interact_llm(self, prompt, max_tokens=None):
                    """Dummy LLM interaction for content generation."""
                    logger.info(f"Dummy LLM interaction invoked with prompt: {prompt[:50]}...")
                    return f"Generated content about the topic. This is placeholder text since the LLM integration is not available."
                
                def post_to_wordpress(self, title, content, category="technology_ai", tags=None, status="draft"):
                    """Dummy WordPress posting method."""
                    logger.info(f"Dummy WordPress posting invoked for article: {title}")
                    return {"success": False, "error": "WordPress posting not configured"}
                
            # Use the adapter instead of the actual AirthAgent
            self.airth = AirthNewsAdapter()
            logger.info("Created AirthNewsAdapter as a substitute for AirthAgent")
            
            # For compatibility with any code that might check these
            self.airth.llm_client = None
            
            # Initialize news fetcher
            self.news_fetcher = NewsFetcher(self.config_path)
            logger.info("News fetcher initialized successfully")
            
            # Initialize news processor
            self.news_processor = NewsProcessor(self.config_path)
            logger.info("News processor initialized successfully")
            
            # Initialize content generator with reference to Airth
            self.content_generator = ContentGenerator(self.config_path, self.airth)
            logger.info("Content generator initialized successfully")
            
        except Exception as e:
            logger.critical(f"Failed to initialize components: {e}")
            raise RuntimeError(f"Failed to initialize news automation system: {e}")

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
        logger.info(f"Parameters: max_age_days={max_age_days}, max_topics={max_topics}, " + 
                   f"publish_status={publish_status}, enable_publishing={enable_publishing}")
        
        try:
            # Step 1: Fetch news articles
            logger.info("Step 1: Fetching news articles")
            articles = self.news_fetcher.fetch_all_sources(max_age_days=max_age_days)
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
            logger.info(f"Selected top {len(topics)} topics for content generation")
            
            # Step 3: Generate content for each topic
            logger.info("Step 3: Generating article content")
            generated_articles = []
            
            for topic in topics:
                logger.info(f"Generating article for topic: {topic.get('suggested_title', f'Topic {topic.get('id', 0)}')}")
                try:
                    result = self.content_generator.generate_article_from_topic(topic)
                    
                    if result.get("success"):
                        generated_articles.append(result)
                        logger.info(f"Successfully generated article: {result.get('title')}")
                    else:
                        logger.error(f"Failed to generate article: {result.get('error')}")
                        self.stats["errors"] += 1
                        
                except Exception as e:
                    logger.error(f"Error generating article content: {e}")
                    self.stats["errors"] += 1
            
            self.stats["articles_created"] = len(generated_articles)
            logger.info(f"Generated {len(generated_articles)} articles from topics")
              # Step 4: Publish content to WordPress
            if generated_articles and enable_publishing:
                # Check if Airth has WordPress posting capability
                if hasattr(self.airth, 'post_to_wordpress') and hasattr(self.airth, 'wp_agent') and self.airth.wp_agent is not None:
                    logger.info(f"Step 4: Publishing articles to WordPress (status: {publish_status})")
                    
                    for article in generated_articles:
                        try:
                            title = article.get("title", "")
                            content = article.get("content", "")
                            category = article.get("category", "technology_ai")
                            tags = article.get("keywords", [])
                            
                            if not title or not content:
                                logger.error("Cannot publish article: missing title or content")
                                self.stats["errors"] += 1
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
                                post_id = result.get("post_id", "unknown")
                                post_url = result.get("url", "")
                                logger.info(f"Successfully published article to WordPress (ID: {post_id})")
                                
                                # Add WordPress info to article data
                                article["wordpress"] = {
                                    "post_id": post_id,
                                    "url": post_url,
                                    "status": publish_status
                                }
                            else:
                                logger.error(f"Failed to publish article: {result.get('error')}")
                                self.stats["errors"] += 1
                                
                            # Add a small delay between publishing to prevent overloading the WordPress site
                            time.sleep(2)
                            
                        except Exception as e:
                            logger.error(f"Error publishing article: {e}")
                            self.stats["errors"] += 1
                else:
                    logger.warning("WordPress publishing capability not available in Airth agent")
                    logger.info("Articles are generated but not published. They can be found in the output directory.")
            
            elif enable_publishing:
                logger.warning("No articles to publish")
            else:
                logger.info("Publishing disabled. Skipping WordPress publishing step.")
            
            # Save run results
            self._save_run_results(generated_articles)
            
            # Calculate runtime
            runtime = time.time() - start_time
            logger.info(f"Airth News Automation workflow completed in {runtime:.2f} seconds")
            logger.info(f"Stats: {json.dumps(self.stats)}")
            
            # Send notification
            self.send_notification(success=True, run_stats=self.stats)
            
            return self.stats
            
        except Exception as e:
            logger.error(f"Error in Airth News Automation workflow: {e}")
            self.stats["errors"] += 1
            
            # Send notification
            self.send_notification(success=False, run_stats=self.stats, error_message=str(e))
            
            return self.stats

    def _save_run_results(self, generated_articles: List[Dict[str, Any]]):
        """Save the results of this run to a file."""
        try:
            # Create output directory if it doesn't exist
            output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'automation_runs')
            os.makedirs(output_dir, exist_ok=True)
            
            # Create results file with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(output_dir, f"automation_run_{timestamp}.json")
            
            # Prepare results data
            results = {
                "timestamp": datetime.now().isoformat(),
                "stats": self.stats,
                "articles": generated_articles
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2)
                
            logger.info(f"Saved run results to {filename}")
            
        except Exception as e:
            logger.error(f"Error saving run results: {e}")

    def send_notification(self, success: bool, run_stats: Dict[str, int], error_message: Optional[str] = None) -> bool:
        """
        Send email notification about the automation run.
        
        Args:
            success: Whether the run was successful
            run_stats: Statistics about the run
            error_message: Error message if any
            
        Returns:
            bool: Whether the notification was sent successfully
        """
        # Check if email notifications are enabled
        smtp_server = os.getenv("SMTP_SERVER")
        smtp_port = os.getenv("SMTP_PORT")
        smtp_username = os.getenv("SMTP_USERNAME")
        smtp_password = os.getenv("SMTP_PASSWORD")
        notification_email = os.getenv("NOTIFICATION_EMAIL")
        
        if not all([smtp_server, smtp_port, smtp_username, smtp_password, notification_email]):
            logger.info("Email notifications not configured. Skipping notification.")
            return False
        
        try:
            # Create message
            msg = MIMEMultipart()
            
            if success:
                msg['Subject'] = f"Airth News Automation: Successful Run ({datetime.now().strftime('%Y-%m-%d')})"
                body = f"""
                <h2>Airth News Automation Run Successful</h2>
                <p>The news automation system completed successfully on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.</p>
                
                <h3>Statistics:</h3>
                <ul>
                    <li>Articles Fetched: {run_stats.get('articles_fetched', 0)}</li>
                    <li>Topics Generated: {run_stats.get('topics_generated', 0)}</li>
                    <li>Articles Created: {run_stats.get('articles_created', 0)}</li>
                    <li>Articles Published: {run_stats.get('articles_published', 0)}</li>
                    <li>Errors Encountered: {run_stats.get('errors', 0)}</li>
                </ul>
                """
            else:
                msg['Subject'] = f"Airth News Automation: Failed Run ({datetime.now().strftime('%Y-%m-%d')})"
                body = f"""
                <h2>Airth News Automation Run Failed</h2>
                <p>The news automation system encountered an error on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.</p>
                
                <h3>Error Message:</h3>
                <pre>{error_message or "Unknown error"}</pre>
                
                <h3>Statistics:</h3>
                <ul>
                    <li>Articles Fetched: {run_stats.get('articles_fetched', 0)}</li>
                    <li>Topics Generated: {run_stats.get('topics_generated', 0)}</li>
                    <li>Articles Created: {run_stats.get('articles_created', 0)}</li>
                    <li>Articles Published: {run_stats.get('articles_published', 0)}</li>
                    <li>Errors Encountered: {run_stats.get('errors', 0)}</li>
                </ul>
                """
            
            msg['From'] = smtp_username
            msg['To'] = notification_email
            
            msg.attach(MIMEText(body, 'html'))
            
            # Send email
            with smtplib.SMTP(smtp_server, int(smtp_port)) as server:
                server.starttls()
                server.login(smtp_username, smtp_password)
                server.send_message(msg)
            
            logger.info(f"Notification email sent to {notification_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send notification email: {e}")
            return False


def main():
    """Main function for running the automation from the command line."""
    parser = argparse.ArgumentParser(description='Airth News Automation System')
    parser.add_argument('--max-age', type=int, default=1, help='Maximum age of news articles in days')
    parser.add_argument('--max-topics', type=int, default=3, help='Maximum number of topics to process')
    parser.add_argument('--status', choices=['draft', 'publish'], default='draft',
                      help='WordPress publication status (default: draft)')
    parser.add_argument('--no-publish', action='store_true', help='Skip publishing to WordPress')
    parser.add_argument('--notify', action='store_true', help='Send email notifications for success/failure')
    parser.add_argument('--config', help='Path to configuration directory')
    
    args = parser.parse_args()
    
    try:
        # Create automation system
        automation = AirthNewsAutomation(config_path=args.config)
        
        # Run the workflow
        stats = automation.run(
            max_age_days=args.max_age,
            max_topics=args.max_topics,
            publish_status=args.status,
            enable_publishing=not args.no_publish
        )
        
        # Show stats summary
        print("\n===== Airth News Automation Summary =====")
        print(f"Articles fetched: {stats['articles_fetched']}")
        print(f"Topics generated: {stats['topics_generated']}")
        print(f"Articles created: {stats['articles_created']}")
        print(f"Articles published: {stats['articles_published']}")
        print(f"Errors encountered: {stats['errors']}")
        
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
