"""
Content Generator - Transforms processed news data into optimized WordPress articles.
Handles SEO optimization, article structure, image selection, and formatting.
"""
import os
import logging
import json
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
import re
import random
from pathlib import Path

logger = logging.getLogger("TEC.ContentGenerator")

class ContentGenerator:
    """
    Generates optimized WordPress-ready content from processed news topics.
    """
    
    def __init__(self, config_path: Optional[str] = None, airth_agent=None):
        """
        Initialize the ContentGenerator with configuration.
        
        Args:
            config_path: Path to configuration file or directory
            airth_agent: Reference to an AirthAgent instance for LLM interactions
        """
        # Default configuration
        self.output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'generated_content')
        self.content_templates = {}
        self.seo_patterns = {}
        self.min_content_length = 800
        self.max_content_length = 1500
        self.default_category = "technology_ai"
        self.include_images = True
        self.airth_agent = airth_agent
        
        # Ensure output directory exists
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Load configuration if provided
        if config_path:
            self._load_config(config_path)
        
        # Load default templates if not loaded from config
        if not self.content_templates:
            self._load_default_templates()

    def _load_config(self, config_path: str):
        """Load content generator configuration from file."""
        try:
            if os.path.isdir(config_path):
                config_path = os.path.join(config_path, 'content_generator.json')
                
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    config = json.load(f)
                
                # Apply configuration values
                self.content_templates = config.get('templates', self.content_templates)
                self.seo_patterns = config.get('seo_patterns', self.seo_patterns)
                self.min_content_length = config.get('min_content_length', self.min_content_length)
                self.max_content_length = config.get('max_content_length', self.max_content_length)
                self.default_category = config.get('default_category', self.default_category)
                self.include_images = config.get('include_images', self.include_images)
                
                if 'output_dir' in config:
                    self.output_dir = config['output_dir']
                    # Ensure output directory exists
                    os.makedirs(self.output_dir, exist_ok=True)
                
                logger.info(f"Loaded content generator configuration from {config_path}")
            else:
                logger.warning(f"Config file not found at {config_path}. Using default configuration.")
                self._load_default_templates()
        except Exception as e:
            logger.error(f"Error loading content generator configuration: {e}")
            self._load_default_templates()

    def _load_default_templates(self):
        """Load default content templates."""
        self.content_templates = {
            "news_roundup": {
                "title": "{{primary_keyword}}: The Latest News and Developments",
                "intro": "The world of {{primary_keyword}} continues to evolve at a rapid pace. In this article, we explore the latest developments and what they mean for the future.",
                "section_format": "<h2>{{section_title}}</h2>\n<p>{{section_content}}</p>",
                "conclusion": "As we've seen, the landscape of {{primary_keyword}} is constantly changing. Stay tuned as we continue to monitor these developments and their implications for the industry.",
                "call_to_action": "What's your take on these recent developments in {{primary_keyword}}? Share your thoughts in the comments below!"
            },
            "deep_dive": {
                "title": "Deep Dive: Understanding the Impact of {{primary_keyword}}",
                "intro": "{{primary_keyword}} is transforming how we think about technology and its role in society. Let's explore the nuances and implications of these recent developments.",
                "section_format": "<h2>{{section_title}}</h2>\n<p>{{section_content}}</p>",
                "conclusion": "The evolution of {{primary_keyword}} represents a significant shift in our technological landscape. By understanding these developments, we can better prepare for what lies ahead.",
                "call_to_action": "How do you see {{primary_keyword}} affecting your industry or daily life? Join the conversation below!"
            },
            "analysis": {
                "title": "Analysis: What {{primary_keyword}} Means for the Future of Tech",
                "intro": "Recent developments in {{primary_keyword}} have sparked important conversations about where technology is headed. In this analysis, we break down the key points and their significance.",
                "section_format": "<h2>{{section_title}}</h2>\n<p>{{section_content}}</p>",
                "conclusion": "While it's impossible to predict exactly how {{primary_keyword}} will evolve, the trends we're seeing suggest a fascinating path forward. The implications for technology, business, and society are profound.",
                "call_to_action": "What aspects of {{primary_keyword}} are you most excited or concerned about? Let us know in the comments!"
            }
        }
        
        self.seo_patterns = {
            "title_formats": [
                "{{primary_keyword}}: {{secondary_aspect}} Explained",
                "The Ultimate Guide to {{primary_keyword}} in {{current_year}}",
                "How {{primary_keyword}} is Changing {{related_industry}}",
                "{{number}} Ways {{primary_keyword}} is Revolutionizing Technology",
                "The Future of {{primary_keyword}}: Trends and Predictions"
            ],
            "meta_description_formats": [
                "Discover the latest developments in {{primary_keyword}} and how they're shaping the future of technology. Learn about {{secondary_aspect}} and more in our comprehensive analysis.",
                "Explore how {{primary_keyword}} is transforming {{related_industry}} with innovative approaches to {{secondary_aspect}}. Stay ahead with our expert insights.",
                "Looking to understand {{primary_keyword}}? Our analysis covers {{secondary_aspect}} and provides actionable insights for navigating this evolving landscape."
            ],
            "heading_patterns": [
                "The Rise of {{primary_keyword}}",
                "Understanding {{secondary_aspect}}",
                "Key Developments in {{primary_keyword}}",
                "How {{primary_keyword}} Impacts {{related_industry}}",
                "Expert Opinions on {{primary_keyword}}",
                "The Future of {{secondary_aspect}}"
            ]
        }
        
        logger.info("Loaded default content templates and SEO patterns")

    def generate_article_from_topic(self, topic_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a complete WordPress-ready article from a processed news topic.
        
        Args:
            topic_data: Processed topic data from the NewsProcessor
            
        Returns:
            Dictionary with the generated article content and metadata
        """
        if not topic_data:
            logger.error("No topic data provided for content generation")
            return {"success": False, "error": "No topic data provided"}
            
        try:
            # Choose template type based on topic characteristics
            template_type = self._select_template_type(topic_data)
            template = self.content_templates.get(template_type)
            
            if not template:
                logger.error(f"Template type '{template_type}' not found")
                return {"success": False, "error": f"Template type '{template_type}' not found"}
            
            # Extract primary keyword and related terms
            primary_keyword = self._extract_primary_keyword(topic_data)
            secondary_aspects = self._extract_secondary_aspects(topic_data)
            related_industry = self._extract_related_industry(topic_data)
            
            # Generate SEO-optimized title
            title = self._generate_title(topic_data, primary_keyword, secondary_aspects)
            
            # Generate article sections
            sections = self._generate_content_sections(topic_data, primary_keyword, secondary_aspects, template)
            
            # Construct full article content
            current_year = datetime.now().year
            article_content = self._construct_article_content(
                template, 
                primary_keyword, 
                secondary_aspects[0] if secondary_aspects else "", 
                related_industry,
                current_year,
                sections
            )
            
            # Generate meta description for SEO
            meta_description = self._generate_meta_description(
                primary_keyword, 
                secondary_aspects[0] if secondary_aspects else "",
                related_industry,
                current_year
            )
            
            # Extract and prepare tags
            tags = self._prepare_tags(topic_data)
            
            # Select appropriate WordPress category
            category = self._select_category(topic_data)
            
            # Save the generated content
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(self.output_dir, f"article_{timestamp}.json")
            
            article_data = {
                "title": title,
                "content": article_content,
                "meta_description": meta_description,
                "keywords": tags,
                "category": category,
                "template_used": template_type,
                "topic_data": {
                    "id": topic_data.get("id"),
                    "suggested_title": topic_data.get("suggested_title"),
                    "keywords": topic_data.get("keywords", [])[:5],  # Limit to top 5 keywords
                    "article_count": topic_data.get("article_count", 0),
                    "sentiment": topic_data.get("sentiment", {}).get("overall", "neutral")
                },
                "generated_at": datetime.now().isoformat()
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(article_data, f, indent=2)
                
            logger.info(f"Generated article: '{title}', saved to {filename}")
            
            # Return the article data with success flag
            return {"success": True, **article_data}
            
        except Exception as e:
            logger.error(f"Error generating article from topic: {e}")
            return {"success": False, "error": str(e)}

    def _select_template_type(self, topic_data: Dict[str, Any]) -> str:
        """
        Select the most appropriate template type based on topic characteristics.
        
        Args:
            topic_data: Processed topic data
            
        Returns:
            Template type identifier string
        """
        # Consider sentiment, article count, and topic dominance
        sentiment = topic_data.get("sentiment", {}).get("overall", "neutral")
        article_count = topic_data.get("article_count", 0)
        
        if article_count >= 10:
            # For topics with many articles, a roundup format works well
            return "news_roundup"
        elif sentiment != "neutral" or topic_data.get("relevance_score", 0) > 0.7:
            # For emotionally charged or highly relevant topics, analysis is better
            return "analysis"
        else:
            # For other cases, a deep dive is appropriate
            return "deep_dive"

    def _extract_primary_keyword(self, topic_data: Dict[str, Any]) -> str:
        """Extract the primary keyword from topic data."""
        # Start with the first keyword if available
        keywords = topic_data.get("keywords", [])
        if keywords:
            return keywords[0]
            
        # Use the most frequent term from dominant terms
        dominant_terms = topic_data.get("dominant_terms", [])
        if dominant_terms:
            return dominant_terms[0]
            
        # Fallback to a generic term based on the suggested title
        suggested_title = topic_data.get("suggested_title", "")
        if suggested_title:
            words = re.findall(r'\b[A-Z][a-z]+\b', suggested_title)
            if words:
                return words[0]
        
        # Last resort fallback
        return "Technology Trends"

    def _extract_secondary_aspects(self, topic_data: Dict[str, Any]) -> List[str]:
        """Extract secondary aspects or subtopics from topic data."""
        aspects = []
        
        # Use additional keywords
        keywords = topic_data.get("keywords", [])
        if len(keywords) > 1:
            aspects.extend(keywords[1:4])  # Take up to 3 additional keywords
            
        # Use additional dominant terms
        dominant_terms = topic_data.get("dominant_terms", [])
        if len(dominant_terms) > 1:
            for term in dominant_terms[1:4]:
                if term not in aspects:
                    aspects.append(term)
        
        # Ensure we have at least some aspects
        if not aspects and topic_data.get("articles"):
            # Extract some words from article titles
            for article in topic_data["articles"][:3]:
                title = article.get("title", "")
                words = re.findall(r'\b[A-Za-z][a-z]{5,}\b', title)
                for word in words:
                    if word.lower() not in [a.lower() for a in aspects]:
                        aspects.append(word)
                        break
        
        return aspects[:5]  # Limit to 5 aspects

    def _extract_related_industry(self, topic_data: Dict[str, Any]) -> str:
        """Extract or infer the related industry from topic data."""
        # Check for industry-specific keywords
        tech_industries = {
            "AI": ["artificial intelligence", "machine learning", "neural network", "deep learning"],
            "Cloud Computing": ["cloud", "aws", "azure", "google cloud", "saas", "paas", "iaas"],
            "Cybersecurity": ["security", "cyber", "hack", "breach", "encryption", "firewall"],
            "Blockchain": ["blockchain", "crypto", "bitcoin", "ethereum", "token", "defi", "nft"],
            "IoT": ["iot", "internet of things", "connected device", "smart home", "sensor"],
            "Mobile Technology": ["mobile", "smartphone", "app", "android", "ios", "5g"],
            "Software Development": ["software", "development", "programming", "code", "api", "sdk"],
            "Data Science": ["data science", "big data", "analytics", "visualization", "database"]
        }
        
        # Combine all text for industry detection
        all_text = ""
        keywords = " ".join(topic_data.get("keywords", []))
        dominant_terms = " ".join(topic_data.get("dominant_terms", []))
        summary = topic_data.get("summary", "")
        all_text = f"{keywords} {dominant_terms} {summary}".lower()
        
        # Find matches
        industry_matches = {}
        for industry, terms in tech_industries.items():
            count = sum(1 for term in terms if term in all_text)
            if count > 0:
                industry_matches[industry] = count
        
        # Return the industry with most matches
        if industry_matches:
            return max(industry_matches.items(), key=lambda x: x[1])[0]
            
        # Fallback
        return "Technology"

    def _generate_title(self, topic_data: Dict[str, Any], primary_keyword: str, secondary_aspects: List[str]) -> str:
        """
        Generate an SEO-optimized title for the article.
        
        Args:
            topic_data: The processed topic data
            primary_keyword: The main keyword for the article
            secondary_aspects: List of secondary aspects or subtopics
            
        Returns:
            Generated title string
        """
        # Try to use a suggested title from the topic data if it's good
        suggested_title = topic_data.get("suggested_title", "")
        if (suggested_title and 
            len(suggested_title) > 20 and 
            len(suggested_title) < 70 and
            primary_keyword.lower() in suggested_title.lower()):
            return suggested_title
            
        # Otherwise, use SEO title patterns
        title_formats = self.seo_patterns.get("title_formats", [])
        if not title_formats:
            return f"{primary_keyword}: Latest News and Developments"
            
        # Select a random title format
        title_format = random.choice(title_formats)
        
        # Fill in the template
        secondary_aspect = secondary_aspects[0] if secondary_aspects else "Latest Developments"
        current_year = str(datetime.now().year)
        related_industry = self._extract_related_industry(topic_data)
        number = random.choice(["5", "7", "10"])
        
        title = title_format.replace("{{primary_keyword}}", primary_keyword)
        title = title.replace("{{secondary_aspect}}", secondary_aspect)
        title = title.replace("{{current_year}}", current_year)
        title = title.replace("{{related_industry}}", related_industry)
        title = title.replace("{{number}}", number)
        
        # Limit length and ensure proper capitalization
        if len(title) > 70:
            title = title[:67] + "..."
        
        return title

    def _generate_content_sections(self, topic_data: Dict[str, Any], primary_keyword: str, 
                                 secondary_aspects: List[str], template: Dict[str, str]) -> List[Dict[str, str]]:
        """
        Generate content sections for the article.
        
        Args:
            topic_data: Processed topic data
            primary_keyword: The main keyword for the article
            secondary_aspects: List of secondary aspects or subtopics
            template: The selected article template
            
        Returns:
            List of section dictionaries with titles and content
        """
        sections = []
        
        # Use heading patterns from SEO patterns
        heading_patterns = self.seo_patterns.get("heading_patterns", [])
        if not heading_patterns:
            # Fallback heading patterns
            heading_patterns = [
                "The Rise of {{primary_keyword}}",
                "Understanding {{secondary_aspect}}",
                "Key Developments in {{primary_keyword}}",
                "How {{primary_keyword}} Impacts {{related_industry}}",
                "Expert Opinions on {{primary_keyword}}",
                "The Future of {{secondary_aspect}}"
            ]
            
        # Determine how many sections to create
        num_sections = min(len(topic_data.get("articles", [])) // 2 + 1, 4)
        num_sections = max(num_sections, 2)  # At least 2 sections
        
        # Generate sections
        related_industry = self._extract_related_industry(topic_data)
        
        for i in range(num_sections):
            # Select a heading pattern
            heading_pattern = heading_patterns[i % len(heading_patterns)]
            
            # Select secondary aspect for this section
            secondary_aspect = secondary_aspects[i % len(secondary_aspects)] if secondary_aspects else "recent developments"
            
            # Generate section title
            section_title = heading_pattern.replace("{{primary_keyword}}", primary_keyword)
            section_title = section_title.replace("{{secondary_aspect}}", secondary_aspect)
            section_title = section_title.replace("{{related_industry}}", related_industry)
            
            # Generate section content using relevant articles
            section_content = self._generate_section_content(topic_data, i, primary_keyword, secondary_aspect)
            
            sections.append({
                "title": section_title,
                "content": section_content
            })
        
        return sections

    def _generate_section_content(self, topic_data: Dict[str, Any], section_index: int, 
                                primary_keyword: str, secondary_aspect: str) -> str:
        """Generate content for a specific article section."""
        # Group articles by relevance to this section
        relevant_articles = topic_data.get("articles", [])
        
        # No articles available
        if not relevant_articles:
            # Generate generic content
            return f"The field of {primary_keyword} continues to evolve, with new developments in {secondary_aspect} being particularly noteworthy. Industry experts suggest that these advancements will have significant implications for how we understand and interact with technology in the coming years."
            
        # Select articles for this section
        section_size = max(1, len(relevant_articles) // 3)
        start_idx = section_index * section_size
        end_idx = start_idx + section_size
        section_articles = relevant_articles[start_idx:end_idx]
        
        # If we have the Airth agent, use it to generate coherent content
        if self.airth_agent:
            # Prepare article data for the prompt
            article_data = []
            for article in section_articles:
                article_data.append({
                    "title": article.get("title", ""),
                    "summary": article.get("summary", ""),
                    "source": article.get("source", "")
                })
                
            # Generate content using Airth's LLM
            try:
                prompt = f"""Write a coherent paragraph or two about {primary_keyword}, focusing on {secondary_aspect}, using information from these articles:

{json.dumps(article_data, indent=2)}

The content should be informative, engaging, and flow naturally. Include relevant details from the articles while maintaining a cohesive narrative. Avoid simply listing facts from each article. Instead, synthesize the information into insightful analysis that would be valuable for readers interested in {primary_keyword}.

Make the text SEO-friendly by naturally incorporating the terms '{primary_keyword}' and '{secondary_aspect}' without keyword stuffing."""

                generated_content = self.airth_agent._interact_llm(prompt, max_tokens=500)
                
                if generated_content and "Error:" not in generated_content:
                    return generated_content
                    
            except Exception as e:
                logger.error(f"Error generating section content with Airth: {e}")
                # Fall back to basic content generation below
        
        # Basic content generation without LLM
        paragraphs = []
        
        # Intro paragraph
        paragraphs.append(f"Recent developments in {primary_keyword} have brought significant attention to {secondary_aspect}. Industry watchers and technology experts alike are taking notice of these advancements.")
        
        # Information from articles
        for article in section_articles:
            title = article.get("title", "")
            summary = article.get("summary", "")
            source = article.get("source", "")
            
            if summary:
                # Extract a sentence or two from the summary
                sentences = re.split(r'[.!?]+', summary)
                sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
                
                if sentences:
                    excerpt = ". ".join(sentences[:2]) + "."
                    paragraph = f"{excerpt} This insight from {source} highlights the importance of understanding how {primary_keyword} continues to evolve."
                    paragraphs.append(paragraph)
        
        # Concluding thoughts
        paragraphs.append(f"As these developments continue to unfold, the relationship between {primary_keyword} and {secondary_aspect} will likely remain a key area of focus for industry professionals.")
        
        # Combine paragraphs
        return "\n\n".join(paragraphs)

    def _construct_article_content(self, template: Dict[str, str], primary_keyword: str, 
                                 secondary_aspect: str, related_industry: str,
                                 current_year: int, sections: List[Dict[str, str]]) -> str:
        """
        Construct the full article content from template and sections.
        
        Args:
            template: Article template to use
            primary_keyword: Main keyword for the article
            secondary_aspect: Secondary aspect or subtopic
            related_industry: Related industry
            current_year: Current year
            sections: Generated content sections
            
        Returns:
            Complete article HTML content
        """
        # Start with intro
        intro = template.get("intro", "")
        intro = intro.replace("{{primary_keyword}}", primary_keyword)
        intro = intro.replace("{{secondary_aspect}}", secondary_aspect)
        intro = intro.replace("{{related_industry}}", related_industry)
        intro = intro.replace("{{current_year}}", str(current_year))
        
        content = f"<p>{intro}</p>\n\n"
        
        # Add each section
        section_format = template.get("section_format", "<h2>{{section_title}}</h2>\n<p>{{section_content}}</p>")
        for section in sections:
            section_content = section_format.replace("{{section_title}}", section["title"])
            section_content = section_content.replace("{{section_content}}", section["content"])
            content += f"{section_content}\n\n"
        
        # Add conclusion
        conclusion = template.get("conclusion", "")
        conclusion = conclusion.replace("{{primary_keyword}}", primary_keyword)
        conclusion = conclusion.replace("{{secondary_aspect}}", secondary_aspect)
        conclusion = conclusion.replace("{{related_industry}}", related_industry)
        conclusion = conclusion.replace("{{current_year}}", str(current_year))
        
        content += f"<h2>Conclusion</h2>\n<p>{conclusion}</p>\n\n"
        
        # Add call to action
        call_to_action = template.get("call_to_action", "")
        call_to_action = call_to_action.replace("{{primary_keyword}}", primary_keyword)
        call_to_action = call_to_action.replace("{{secondary_aspect}}", secondary_aspect)
        call_to_action = call_to_action.replace("{{related_industry}}", related_industry)
        call_to_action = call_to_action.replace("{{current_year}}", str(current_year))
        
        content += f"<p>{call_to_action}</p>"
        
        return content

    def _generate_meta_description(self, primary_keyword: str, secondary_aspect: str,
                                 related_industry: str, current_year: int) -> str:
        """Generate an SEO-optimized meta description for the article."""
        # Use meta description formats from SEO patterns
        meta_formats = self.seo_patterns.get("meta_description_formats", [])
        if not meta_formats:
            return f"Explore the latest developments in {primary_keyword} and {secondary_aspect}. Learn how these innovations are transforming {related_industry} in {current_year} and beyond."
            
        # Select a random format
        meta_format = random.choice(meta_formats)
        
        # Fill in the template
        meta_description = meta_format.replace("{{primary_keyword}}", primary_keyword)
        meta_description = meta_description.replace("{{secondary_aspect}}", secondary_aspect)
        meta_description = meta_description.replace("{{related_industry}}", related_industry)
        meta_description = meta_description.replace("{{current_year}}", str(current_year))
        
        # Limit length
        if len(meta_description) > 160:
            meta_description = meta_description[:157] + "..."
        
        return meta_description

    def _prepare_tags(self, topic_data: Dict[str, Any]) -> List[str]:
        """Prepare WordPress tags from topic data."""
        tags = []
        
        # Add main keywords
        if "keywords" in topic_data:
            tags.extend(topic_data["keywords"][:10])  # Limit to top 10
        
        # Add some dominant terms if needed
        if "dominant_terms" in topic_data and len(tags) < 10:
            for term in topic_data["dominant_terms"]:
                if term not in tags and len(tags) < 10:
                    tags.append(term)
        
        # Add sentiment as a tag if strong
        if "sentiment" in topic_data:
            sentiment = topic_data["sentiment"].get("overall", "neutral")
            if sentiment != "neutral":
                sentiment_tag = f"{sentiment} tech trends"
                if sentiment_tag not in tags:
                    tags.append(sentiment_tag)
        
        # Add industry as a tag
        related_industry = self._extract_related_industry(topic_data)
        if related_industry and related_industry not in tags:
            tags.append(related_industry)
            
        return tags

    def _select_category(self, topic_data: Dict[str, Any]) -> str:
        """Select appropriate WordPress category based on topic."""
        # Extract and analyze topic characteristics
        categories = {
            "airths_codex": ["analysis", "future", "prediction", "opinion", "perspective"],
            "technology_ai": ["ai", "machine learning", "artificial intelligence", "automation", "algorithm"],
            "creative_explorations": ["design", "creative", "art", "innovation", "imagination"],
            "workflows_automation": ["workflow", "productivity", "automation", "tools", "software"]
        }
        
        # Combine all text for category detection
        all_text = ""
        keywords = " ".join(topic_data.get("keywords", []))
        dominant_terms = " ".join(topic_data.get("dominant_terms", []))
        summary = topic_data.get("summary", "")
        all_text = f"{keywords} {dominant_terms} {summary}".lower()
        
        # Find matches
        category_matches = {}
        for category, terms in categories.items():
            count = sum(1 for term in terms if term in all_text)
            category_matches[category] = count
        
        # Select category with most matches, or default
        if any(count > 0 for count in category_matches.values()):
            return max(category_matches.items(), key=lambda x: x[1])[0]
            
        # Fallback to default
        return self.default_category


if __name__ == "__main__":
    # Configure logging for standalone testing
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Test content generation with sample data
    generator = ContentGenerator()
    
    # Sample topic data 
    sample_topic = {
        "id": 1,
        "suggested_title": "The Rise of AI in Healthcare: Transforming Patient Outcomes",
        "keywords": ["AI in Healthcare", "Machine Learning", "Patient Care", "Diagnostics", "Medical Innovation"],
        "dominant_terms": ["healthcare", "AI", "diagnosis", "patient", "algorithm", "treatment"],
        "article_count": 7,
        "relevance_score": 0.85,
        "sentiment": {
            "compound": 0.6,
            "positive": 0.8,
            "negative": 0.1,
            "neutral": 0.1,
            "overall": "positive"
        },
        "summary": "AI technologies are revolutionizing healthcare by improving diagnostic accuracy and treatment recommendations. Recent studies show that AI-assisted diagnoses can reduce errors by up to 40% in certain medical fields.",
        "articles": [
            {
                "title": "New AI System Outperforms Doctors in Diagnosing Rare Diseases",
                "source": "Medical Journal",
                "summary": "A newly developed AI system has demonstrated superior performance in diagnosing rare diseases compared to experienced physicians. The system, developed by researchers at Stanford, analyzed thousands of patient records to identify patterns that human doctors might miss."
            },
            {
                "title": "Healthcare Providers Increasingly Adopt AI Tools for Patient Care",
                "source": "Health Tech Today",
                "summary": "Major hospitals across the country are implementing AI-powered tools to assist with patient care. These tools help predict patient deterioration, optimize treatment plans, and improve resource allocation."
            },
            {
                "title": "Ethical Concerns Rise as AI Makes Medical Decisions",
                "source": "Ethics in Medicine",
                "summary": "As AI takes on more responsibility in healthcare decision-making, ethicists raise concerns about accountability, transparency, and potential biases in algorithms that could affect patient outcomes."
            }
        ]
    }
    
    # Generate article
    result = generator.generate_article_from_topic(sample_topic)
    
    # Display results
    if result.get("success"):
        print(f"Generated Article: {result['title']}")
        print(f"Category: {result['category']}")
        print(f"Keywords: {', '.join(result['keywords'])}")
        print(f"Meta Description: {result['meta_description']}")
        print("\nContent Preview:")
        preview_length = min(500, len(result['content']))
        print(f"{result['content'][:preview_length]}...")
    else:
        print(f"Error: {result.get('error')}")
