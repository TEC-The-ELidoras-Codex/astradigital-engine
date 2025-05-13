"""
Common utility functions for TEC_OFFICE_REPO.
"""
import os
import logging
import json
from datetime import datetime
from typing import Dict, Any, Optional, List, Union

# Configure logging
logger = logging.getLogger("TEC.Utils")


def load_json_file(file_path: str, default_value: Any = None) -> Any:
    """
    Load data from a JSON file with error handling.
    
    Args:
        file_path: Path to the JSON file
        default_value: Value to return if the file doesn't exist or there's an error
        
    Returns:
        The data from the JSON file or the default value
    """
    try:
        if not os.path.exists(file_path):
            logger.warning(f"File not found: {file_path}")
            return default_value
            
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        logger.debug(f"Successfully loaded data from {file_path}")
        return data
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in {file_path}: {e}")
        return default_value
    except Exception as e:
        logger.error(f"Error loading {file_path}: {e}")
        return default_value


def save_json_file(file_path: str, data: Any, indent: int = 2) -> bool:
    """
    Save data to a JSON file with error handling.
    
    Args:
        file_path: Path to the JSON file
        data: Data to save
        indent: Indentation level for the JSON file
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent, ensure_ascii=False)
            
        logger.debug(f"Successfully saved data to {file_path}")
        return True
    except Exception as e:
        logger.error(f"Error saving to {file_path}: {e}")
        return False


def get_timestamp() -> str:
    """
    Get the current timestamp in ISO format.
    
    Returns:
        Current timestamp string
    """
    return datetime.now().isoformat()


def sanitize_filename(filename: str) -> str:
    """
    Sanitize a filename to ensure it's valid across operating systems.
    
    Args:
        filename: The filename to sanitize
        
    Returns:
        Sanitized filename
    """
    # Replace invalid characters
    invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for char in invalid_chars:
        filename = filename.replace(char, '_')
        
    # Ensure the filename isn't just spaces or dots
    if filename.strip() in ['', '.', '..']:
        filename = "unnamed_file"
        
    return filename


def create_id(prefix: str = "") -> str:
    """
    Create a unique ID based on timestamp.
    
    Args:
        prefix: Optional prefix for the ID
        
    Returns:
        Unique ID string
    """
    from datetime import datetime
    import random
    
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    random_suffix = ''.join(random.choices('0123456789abcdef', k=4))
    
    if prefix:
        return f"{prefix}_{timestamp}_{random_suffix}"
    else:
        return f"{timestamp}_{random_suffix}"


def merge_dicts(dict1: Dict[str, Any], dict2: Dict[str, Any], 
                overwrite: bool = True) -> Dict[str, Any]:
    """
    Merge two dictionaries with nested dictionaries.
    
    Args:
        dict1: First dictionary
        dict2: Second dictionary
        overwrite: Whether to overwrite values in dict1 with values from dict2
        
    Returns:
        Merged dictionary
    """
    result = dict1.copy()
    
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            # If both are dictionaries, merge them recursively
            result[key] = merge_dicts(result[key], value, overwrite)
        elif key not in result or overwrite:
            # If the key doesn't exist in result or overwrite is True, add/update it
            result[key] = value
            
    return result


def format_exception(e: Exception) -> str:
    """
    Format an exception into a readable string.
    
    Args:
        e: The exception
        
    Returns:
        Formatted exception string
    """
    import traceback
    
    error_type = type(e).__name__
    error_msg = str(e)
    trace = traceback.format_exc()
    
    return f"{error_type}: {error_msg}\n{trace}"
