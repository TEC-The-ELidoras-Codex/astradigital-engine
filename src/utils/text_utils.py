"""
Text utility functions for The Elidoras Codex.
Provides text processing and HTML sanitization capabilities.
"""
import re
from typing import Optional
from html import unescape
from html.parser import HTMLParser


class MLStripper(HTMLParser):
    """HTML tag stripper class."""
    
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = []

    def handle_data(self, data):
        self.text.append(data)

    def get_data(self):
        return ''.join(self.text)


def sanitize_html(html_content: Optional[str]) -> str:
    """
    Sanitize HTML content by removing dangerous tags and attributes.
    
    Args:
        html_content: The HTML content to sanitize
        
    Returns:
        Sanitized HTML string
    """
    if not html_content:
        return ""
    
    # Remove script tags and their content
    html_content = re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
    
    # Remove style tags and their content
    html_content = re.sub(r'<style[^>]*>.*?</style>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
    
    # Remove dangerous attributes (onclick, onload, etc.)
    html_content = re.sub(r'\s*on\w+\s*=\s*["\'][^"\']*["\']', '', html_content, flags=re.IGNORECASE)
    
    # Remove javascript: protocols
    html_content = re.sub(r'javascript:', '', html_content, flags=re.IGNORECASE)
    
    return html_content.strip()


def extract_text_from_html(html_content: Optional[str]) -> str:
    """
    Extract plain text from HTML content.
    
    Args:
        html_content: The HTML content to process
        
    Returns:
        Plain text string with HTML tags removed
    """
    if not html_content:
        return ""
    
    # Create stripper instance
    stripper = MLStripper()
    
    # Parse the HTML
    stripper.feed(html_content)
    
    # Get the text and clean it up
    text = stripper.get_data()
    
    # Unescape HTML entities
    text = unescape(text)
    
    # Clean up whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text


def truncate_text(text: str, max_length: int = 160, suffix: str = "...") -> str:
    """
    Truncate text to a maximum length, adding a suffix if truncated.
    
    Args:
        text: The text to truncate
        max_length: Maximum length of the output
        suffix: Suffix to add if text is truncated
        
    Returns:
        Truncated text string
    """
    if len(text) <= max_length:
        return text
    
    # Find the last space before the max length
    truncate_at = max_length - len(suffix)
    last_space = text.rfind(' ', 0, truncate_at)
    
    if last_space > 0:
        return text[:last_space] + suffix
    else:
        return text[:truncate_at] + suffix


def clean_filename(filename: str) -> str:
    """
    Clean a filename by removing or replacing invalid characters.
    
    Args:
        filename: The filename to clean
        
    Returns:
        Cleaned filename string
    """
    # Remove or replace invalid characters
    cleaned = re.sub(r'[<>:"/\\|?*]', '', filename)
    
    # Replace spaces with underscores
    cleaned = cleaned.replace(' ', '_')
    
    # Remove multiple underscores
    cleaned = re.sub(r'_+', '_', cleaned)
    
    # Strip leading/trailing underscores and dots
    cleaned = cleaned.strip('_.')
    
    return cleaned if cleaned else "untitled"