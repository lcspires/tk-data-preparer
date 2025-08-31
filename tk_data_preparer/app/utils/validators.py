"""
Validation utilities for Tk Data Preparer.
"""

import re
from typing import Optional, Union


def validate_integer(value: Union[str, int], min_value: Optional[int] = None, 
                    max_value: Optional[int] = None) -> bool:
    """
    Validate if value is a valid integer within optional range.
    
    Args:
        value: Value to validate (string or integer)
        min_value: Optional minimum value
        max_value: Optional maximum value
        
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        num = int(value)
        if min_value is not None and num < min_value:
            return False
        if max_value is not None and num > max_value:
            return False
        return True
    except (ValueError, TypeError):
        return False


def validate_filename(filename: str, allowed_extensions: Optional[list] = None) -> bool:
    """
    Validate filename for safe file operations.
    
    Args:
        filename: Filename to validate
        allowed_extensions: Optional list of allowed extensions (e.g. ['.csv', '.xlsx'])
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not filename or not isinstance(filename, str):
        return False
        
    # Check for invalid characters
    invalid_chars = r'[<>:"/\\|?*]'
    if re.search(invalid_chars, filename):
        return False
        
    # Check length
    if len(filename) > 255:
        return False
        
    # Check extension if specified
    if allowed_extensions:
        if not any(filename.lower().endswith(ext.lower()) for ext in allowed_extensions):
            return False
            
    return True


def validate_email(email: str) -> bool:
    """
    Validate email format.
    
    Args:
        email: Email address to validate
        
    Returns:
        bool: True if valid email format, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email)) if email else False


def validate_not_empty(value: str) -> bool:
    """
    Validate that value is not empty or only whitespace.
    
    Args:
        value: String to validate
        
    Returns:
        bool: True if not empty, False otherwise
    """
    return bool(value and str(value).strip())