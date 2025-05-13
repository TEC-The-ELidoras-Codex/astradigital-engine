"""
TEC_OFFICE_REPO WordPress Module
"""
from .wordpress_xmlrpc import WordPressXMLRPC, test_wordpress_connection

__all__ = [
    'WordPressXMLRPC',
    'test_wordpress_connection'
]
