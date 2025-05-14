"""
News Processor - A module for processing and analyzing news data.
Performs topic extraction, sentiment analysis, and content summarization.
"""
import os
import logging
import json
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
import re
from collections import Counter, defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import nltk
from pathlib import Path

logger = logging.getLogger("TEC.NewsProcessor")

class NewsProcessor:
    """
    Handles processing and analysis of news data.
    Identifies trends, extracts topics, and prepares data for content generation.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the NewsProcessor with configuration.
        
        Args:
            config_path: Path to configuration file or directory
        """
        # Download required NLTK data if not already present
        self._ensure_nltk_resources()
        
        self.stop_words = set(stopwords.words('english'))
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        
        # Default configuration
        self.min_articles_per_topic = 3
        self.max_articles_per_topic = 15
        self.min_topic_relevance = 0.5
        self.max_topics = 10
        self.output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'processed_news')
        
        # Ensure output directory exists
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Load configuration if provided
        if config_path:
            self._load_config(config_path)

    def _ensure_nltk_resources(self):
        """Ensure required NLTK resources are downloaded."""
        try:
            resources = [
                'punkt', 
                'stopwords', 
                'vader_lexicon'
            ]
            
            for resource in resources:
                try:
                    nltk.data.find(f'tokenizers/{resource}')
                except LookupError:
                    logger.info(f"Downloading NLTK resource: {resource}")
                    nltk.download(resource, quiet=True)
                    
        except Exception as e:
            logger.error(f"Error ensuring NLTK resources: {e}")
            logger.warning("Some features may not work correctly without NLTK resources")

    def _load_config(self, config_path: str):
        """Load news processor configuration from file."""
        try:
            if os.path.isdir(config_path):
                config_path = os.path.join(config_path, 'news_processor.json')
                
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    config = json.load(f)
                
                # Apply configuration values
                self.min_articles_per_topic = config.get('min_articles_per_topic', self.min_articles_per_topic)
                self.max_articles_per_topic = config.get('max_articles_per_topic', self.max_articles_per_topic)
                self.min_topic_relevance = config.get('min_topic_relevance', self.min_topic_relevance)
                self.max_topics = config.get('max_topics', self.max_topics)
                
                if 'output_dir' in config:
                    self.output_dir = config['output_dir']
                    # Ensure output directory exists
                    os.makedirs(self.output_dir, exist_ok=True)
                
                logger.info(f"Loaded news processor configuration from {config_path}")
            else:
                logger.warning(f"Config file not found at {config_path}. Using default configuration.")
        except Exception as e:
            logger.error(f"Error loading news processor configuration: {e}")
            logger.info("Using default configuration")

    def process_articles(self, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Process a list of news articles to extract topics and insights.
        
        Args:
            articles: List of news articles
            
        Returns:
            List of topic clusters with associated articles and analysis
        """
        if not articles:
            logger.warning("No articles provided for processing")
            return []
            
        logger.info(f"Processing {len(articles)} articles")
        
        # Remove duplicate articles
        unique_articles = self._remove_duplicates(articles)
        logger.info(f"Found {len(unique_articles)} unique articles after deduplication")
        
        # Extract text for topic modeling
        texts = []
        for article in unique_articles:
            # Combine title and content for better topic modeling
            text = f"{article['title']} {article.get('summary', '')}"
            texts.append(text)
        
        # Calculate topics using TF-IDF and clustering
        topics = self._extract_topics(texts, unique_articles)
        logger.info(f"Extracted {len(topics)} topic clusters")
        
        # Analyze sentiment and relevance for each topic
        for topic in topics:
            # Sentiment analysis
            topic_sentiment = self._analyze_topic_sentiment(topic)
            topic["sentiment"] = topic_sentiment
            
            # Overall relevance score
            topic["relevance_score"] = self._calculate_relevance(topic)
            
            # Generate a title for the topic
            topic["suggested_title"] = self._suggest_topic_title(topic)
            
            # Tag the topic with relevant keywords
            topic["keywords"] = self._extract_keywords(topic)
            
            # Create a topic summary
            topic["summary"] = self._create_topic_summary(topic)
        
        # Filter and sort topics by relevance
        relevant_topics = [t for t in topics if t["relevance_score"] >= self.min_topic_relevance]
        relevant_topics.sort(key=lambda x: x["relevance_score"], reverse=True)
        
        # Limit to maximum number of topics
        top_topics = relevant_topics[:self.max_topics]
        
        # Save processed topics
        self._save_processed_topics(top_topics)
        
        return top_topics

    def _remove_duplicates(self, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Remove duplicate articles based on URL and title similarity.
        
        Args:
            articles: List of articles
            
        Returns:
            List of unique articles
        """
        unique_urls = set()
        unique_articles = []
        
        for article in articles:
            url = article.get('url', '')
            
            # Skip articles with no URL
            if not url:
                continue
                
            # Skip duplicate URLs
            if url in unique_urls:
                continue
                
            unique_urls.add(url)
            unique_articles.append(article)
        
        return unique_articles

    def _extract_topics(self, texts: List[str], articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Extract topics from a collection of texts using TF-IDF and K-means clustering.
        
        Args:
            texts: List of article texts
            articles: Original article dictionaries
            
        Returns:
            List of topic dictionaries with clustered articles
        """
        if not texts:
            return []
            
        try:
            # Determine number of clusters
            n_clusters = min(max(3, len(texts) // 5), 10)  # Aim for 3-10 clusters based on volume
            
            # Use TF-IDF to vectorize the texts
            vectorizer = TfidfVectorizer(
                max_df=0.8,
                min_df=2,
                max_features=5000,
                stop_words='english'
            )
            
            # Handle the case when we have too few documents
            if len(texts) < 2:
                # Create a single "topic" with all articles
                return [{
                    "id": 0,
                    "articles": articles,
                    "article_count": len(articles),
                    "dominant_terms": self._extract_terms_from_texts(texts)
                }]
            
            tfidf_matrix = vectorizer.fit_transform(texts)
            
            # Cluster using K-means
            kmeans = KMeans(n_clusters=n_clusters, random_state=42)
            kmeans.fit(tfidf_matrix)
            
            clusters = kmeans.labels_
            
            # Build topic dictionaries
            topics = []
            cluster_articles = defaultdict(list)
            
            # Group articles by cluster
            for i, cluster_id in enumerate(clusters):
                cluster_articles[cluster_id].append(articles[i])
            
            # Get feature names (words) from the vectorizer
            terms = vectorizer.get_feature_names_out()
            
            # For each cluster, extract the top terms
            for cluster_id, cluster_center in enumerate(kmeans.cluster_centers_):
                # Get the most significant terms for this cluster
                ordered_terms = [terms[i] for i in cluster_center.argsort()[-20:]]
                
                topic = {
                    "id": cluster_id,
                    "articles": cluster_articles[cluster_id],
                    "article_count": len(cluster_articles[cluster_id]),
                    "dominant_terms": ordered_terms[::-1]  # Reverse to get most significant first
                }
                topics.append(topic)
            
            # Filter out topics with too few or too many articles
            filtered_topics = []
            for topic in topics:
                if self.min_articles_per_topic <= topic["article_count"] <= self.max_articles_per_topic:
                    filtered_topics.append(topic)
                    
            return filtered_topics
            
        except Exception as e:
            logger.error(f"Error extracting topics: {e}")
            return []

    def _extract_terms_from_texts(self, texts: List[str]) -> List[str]:
        """Extract key terms from a list of texts without using vectorizer."""
        if not texts:
            return []
            
        # Combine all texts
        all_text = " ".join(texts)
        
        # Tokenize and remove stopwords
        words = word_tokenize(all_text.lower())
        words = [w for w in words if w.isalpha() and w not in self.stop_words and len(w) > 2]
        
        # Count word frequencies
        word_counts = Counter(words)
        
        # Return the most common words
        return [word for word, count in word_counts.most_common(20)]

    def _analyze_topic_sentiment(self, topic: Dict[str, Any]) -> Dict[str, float]:
        """
        Analyze the overall sentiment of articles in a topic.
        
        Args:
            topic: Topic dictionary with articles
            
        Returns:
            Dictionary with sentiment scores
        """
        compound_scores = []
        positive_scores = []
        negative_scores = []
        neutral_scores = []
        
        for article in topic["articles"]:
            # Combine title and summary for sentiment analysis
            text = f"{article['title']}. {article.get('summary', '')}"
            
            sentiment = self.sentiment_analyzer.polarity_scores(text)
            
            compound_scores.append(sentiment["compound"])
            positive_scores.append(sentiment["pos"])
            negative_scores.append(sentiment["neg"])
            neutral_scores.append(sentiment["neu"])
        
        # Calculate averages
        avg_compound = sum(compound_scores) / len(compound_scores) if compound_scores else 0
        avg_positive = sum(positive_scores) / len(positive_scores) if positive_scores else 0
        avg_negative = sum(negative_scores) / len(negative_scores) if negative_scores else 0
        avg_neutral = sum(neutral_scores) / len(neutral_scores) if neutral_scores else 0
        
        return {
            "compound": avg_compound,
            "positive": avg_positive,
            "negative": avg_negative,
            "neutral": avg_neutral,
            "overall": "positive" if avg_compound > 0.05 else "negative" if avg_compound < -0.05 else "neutral"
        }

    def _calculate_relevance(self, topic: Dict[str, Any]) -> float:
        """
        Calculate a relevance score for a topic based on several factors.
        
        Args:
            topic: Topic dictionary
            
        Returns:
            Relevance score between 0 and 1
        """
        # Factors for relevance:
        # 1. Number of articles (more is better, up to a point)
        # 2. Sentiment intensity (stronger sentiment, either way, is more relevant)
        # 3. Recency of articles
        # 4. Diversity of sources
        
        # Factor 1: Number of articles
        article_count = topic["article_count"]
        count_score = min(article_count / self.max_articles_per_topic, 1.0)
        
        # Factor 2: Sentiment intensity
        sentiment = topic["sentiment"]
        sentiment_intensity = abs(sentiment["compound"])
          # Factor 3: Recency - average days old (0 = today, lower is better)
        days_old_sum = 0
        now = datetime.now()
        for article in topic["articles"]:
            pub_date = article.get("published_datetime", now)
            
            # Handle string datetime
            if isinstance(pub_date, str):
                try:
                    pub_date = datetime.fromisoformat(pub_date.replace('Z', '+00:00'))
                except ValueError:
                    pub_date = now  # If conversion fails, use current time
            
            days_old = (now - pub_date).total_seconds() / 86400  # Convert to days
            days_old_sum += days_old
            
        avg_days_old = days_old_sum / article_count if article_count > 0 else 7
        recency_score = 1.0 - min(avg_days_old / 7, 1.0)  # 0-7 days old mapped to 1.0-0.0
        
        # Factor 4: Source diversity
        sources = set()
        for article in topic["articles"]:
            sources.add(article.get("source", ""))
            
        source_count = len(sources)
        diversity_score = min(source_count / 5, 1.0)  # Up to 5 different sources
        
        # Combined score with weights
        weights = {
            "count": 0.25,
            "sentiment": 0.2,
            "recency": 0.35,
            "diversity": 0.2
        }
        
        relevance_score = (
            weights["count"] * count_score +
            weights["sentiment"] * sentiment_intensity +
            weights["recency"] * recency_score +
            weights["diversity"] * diversity_score
        )
        
        return relevance_score

    def _suggest_topic_title(self, topic: Dict[str, Any]) -> str:
        """
        Suggest a title for a topic based on its articles and dominant terms.
        
        Args:
            topic: Topic dictionary
            
        Returns:
            Suggested title string
        """
        # Strategy 1: Use the title of the most recent article with some cleaning
        most_recent_date = datetime.min
        most_recent_title = ""
          for article in topic["articles"]:
            pub_date = article.get("published_datetime", datetime.min)
            
            # Handle string datetime
            if isinstance(pub_date, str):
                try:
                    pub_date = datetime.fromisoformat(pub_date.replace('Z', '+00:00'))
                except ValueError:
                    pub_date = datetime.min  # If conversion fails, use min time
            
            if pub_date > most_recent_date:
                most_recent_date = pub_date
                most_recent_title = article.get("title", "")
        
        # Clean the title - remove source markers like "- TechCrunch" at the end
        cleaned_title = re.sub(r'\s+[-–|]\s+\w+(\s+\w+)?$', '', most_recent_title)
        
        # If we have a reasonable title, use it
        if cleaned_title and len(cleaned_title) > 15 and len(cleaned_title) < 100:
            return cleaned_title
            
        # Strategy 2: Combine dominant terms
        if topic["dominant_terms"]:
            terms = topic["dominant_terms"][:4]  # Top 4 terms
            return f"Trending in Tech: {', '.join(term.title() for term in terms)}"
            
        # Fallback
        return "Latest Technology Trends and Developments"

    def _extract_keywords(self, topic: Dict[str, Any]) -> List[str]:
        """
        Extract keywords for a topic.
        
        Args:
            topic: Topic dictionary
            
        Returns:
            List of keyword strings
        """
        # Start with dominant terms
        keywords = topic["dominant_terms"][:10]  # Top 10 terms
        
        # Extract entities from article titles
        all_title_text = " ".join([a.get("title", "") for a in topic["articles"]])
        
        # Simple approach: extract capitalized words that aren't at the beginning of sentences
        title_words = word_tokenize(all_title_text)
        for i, word in enumerate(title_words):
            if (word[0].isupper() and len(word) > 1 and 
                (i == 0 or title_words[i-1] not in ['.', '!', '?']) and
                word.lower() not in self.stop_words):
                if word not in keywords and not any(word.lower() == k.lower() for k in keywords):
                    keywords.append(word)
        
        # Filter out duplicates and lowercase versions of existing keywords
        final_keywords = []
        lowercase_keywords = set()
        
        for keyword in keywords:
            if keyword.lower() not in lowercase_keywords:
                final_keywords.append(keyword)
                lowercase_keywords.add(keyword.lower())
        
        # Limit to top 15 keywords
        return final_keywords[:15]

    def _create_topic_summary(self, topic: Dict[str, Any]) -> str:
        """
        Create a summary of the topic based on its articles.
        
        Args:
            topic: Topic dictionary
            
        Returns:
            Summary string
        """
        # Extract sentences from article summaries
        all_sentences = []
        
        for article in topic["articles"]:
            title = article.get("title", "")
            summary = article.get("summary", "")
            
            # Add the title as a sentence
            if title:
                all_sentences.append(title)
            
            # Extract sentences from the summary
            if summary:
                sentences = sent_tokenize(summary)
                all_sentences.extend(sentences)
        
        # Calculate a rough "importance" score for each sentence
        sentence_importance = {}
        for sentence in all_sentences:
            # Convert to lowercase for matching
            lower_sentence = sentence.lower()
            
            # Count how many dominant terms appear in the sentence
            term_count = sum(1 for term in topic["dominant_terms"] if term.lower() in lower_sentence)
            
            # Basic scoring: term count plus bonus for shorter sentences
            score = term_count + (1 / (len(sentence.split()) + 10))  # +10 to avoid division by zero
            
            sentence_importance[sentence] = score
        
        # Select top sentences
        top_sentences = sorted(all_sentences, key=lambda s: sentence_importance.get(s, 0), reverse=True)
        
        # Take top 3-5 sentences, depending on their length
        total_length = 0
        selected_sentences = []
        
        for sentence in top_sentences:
            if total_length > 500 or len(selected_sentences) >= 5:
                break
                
            if sentence not in selected_sentences:
                selected_sentences.append(sentence)
                total_length += len(sentence)
        
        # Join the selected sentences
        summary = " ".join(selected_sentences)
        
        # If summary is too short, use the top article's summary directly
        if len(summary) < 100 and topic["articles"]:
            top_article = sorted(topic["articles"], 
                                key=lambda a: a.get("published_datetime", datetime.min), 
                                reverse=True)[0]
            summary = top_article.get("summary", summary)
        
        return summary

    def _save_processed_topics(self, topics: List[Dict[str, Any]]):
        """
        Save processed topics to file.
        
        Args:
            topics: List of processed topic dictionaries
        """
        try:
            # Create a timestamped filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(self.output_dir, f"processed_topics_{timestamp}.json")
            
            # Convert datetime objects to ISO strings for JSON serialization
            topics_copy = []
            for topic in topics:
                topic_copy = topic.copy()
                
                # Process articles
                articles_copy = []
                for article in topic_copy["articles"]:
                    article_copy = article.copy()
                    
                    # Convert datetime to string if present
                    if "published_datetime" in article_copy and isinstance(article_copy["published_datetime"], datetime):
                        article_copy["published_datetime"] = article_copy["published_datetime"].isoformat()
                        
                    articles_copy.append(article_copy)
                
                topic_copy["articles"] = articles_copy
                topics_copy.append(topic_copy)
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(topics_copy, f, indent=2)
                
            logger.info(f"Saved processed topics to {filename}")
            
        except Exception as e:
            logger.error(f"Error saving processed topics: {e}")


if __name__ == "__main__":
    # Configure logging for standalone testing
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Test with a small set of articles
    processor = NewsProcessor()
    
    # Define some test articles
    test_articles = [
        {
            "title": "New AI Model Breaks Performance Records",
            "url": "https://example.com/article1",
            "source": "Tech News",
            "published_datetime": datetime.now(),
            "summary": "Researchers have developed a new AI model that outperforms previous benchmarks by 20%. The model uses a novel architecture that combines transformer networks with reinforcement learning techniques."
        },
        {
            "title": "AI Safety Concerns Grow Among Researchers",
            "url": "https://example.com/article2",
            "source": "Science Daily",
            "published_datetime": datetime.now(),
            "summary": "Leading AI researchers express concerns about the rapid development of artificial intelligence without adequate safety measures. Many call for new regulations and oversight."
        },
        {
            "title": "Tech Giants Announce New AI Safety Coalition",
            "url": "https://example.com/article3",
            "source": "Business Insider",
            "published_datetime": datetime.now(),
            "summary": "Major technology companies have formed a new coalition focused on ensuring the safe development of artificial intelligence. The group plans to establish industry standards and best practices."
        }
    ]
    
    topics = processor.process_articles(test_articles)
    
    # Display results
    for topic in topics:
        print("\n----- Topic -----")
        print(f"Title: {topic['suggested_title']}")
        print(f"Keywords: {', '.join(topic['keywords'])}")
        print(f"Sentiment: {topic['sentiment']['overall']} (score: {topic['sentiment']['compound']:.2f})")
        print(f"Relevance: {topic['relevance_score']:.2f}")
        print(f"Summary: {topic['summary']}")
        print(f"Article count: {topic['article_count']}")
        print("Articles:")
        for i, article in enumerate(topic['articles'][:3]):
            print(f"  {i+1}. {article['title']} ({article['source']})")
