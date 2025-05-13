"""
Unit tests for core TEC utilities.
"""
import os
import sys
import pytest
from pathlib import Path

# Add the parent directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Try to import from source
try:
    from src.utils.text_utils import sanitize_html, extract_text_from_html
    HAS_UTILS = True
except ImportError:
    HAS_UTILS = False
    
# Skip all tests if utils are not available
pytestmark = pytest.mark.skipif(not HAS_UTILS, reason="Core utils not available")

class TestTextUtils:
    """Test the text utility functions."""
    
    def test_sanitize_html(self):
        """Test sanitizing HTML content."""
        test_html = '<p>This is a <b>test</b> with <script>alert("XSS")</script> content.</p>'
        expected = '<p>This is a <b>test</b> with  content.</p>'
        
        result = sanitize_html(test_html)
        assert result == expected, f"HTML sanitization failed, got: {result}"
        
    def test_extract_text_from_html(self):
        """Test extracting plain text from HTML."""
        test_html = '<p>This is a <b>test</b> with <a href="https://example.com">link</a>.</p>'
        expected = 'This is a test with link.'
        
        result = extract_text_from_html(test_html)
        assert result == expected, f"Text extraction failed, got: {result}"
    
    def test_sanitize_empty_input(self):
        """Test sanitizing empty input."""
        result = sanitize_html("")
        assert result == "", "Empty input should return empty output"
        
    def test_sanitize_none_input(self):
        """Test sanitizing None input."""
        result = sanitize_html(None)
        assert result == "", "None input should return empty string"
