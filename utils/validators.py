"""
Data validation utilities
"""

import validators
from typing import Dict, Any


def validate_url(url: str) -> bool:
    """
    Validate if a string is a valid URL
    
    Args:
        url: URL string to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not url:
        return False
    
    result = validators.url(url)
    return result is True


def validate_product_data(product: Dict[str, Any]) -> bool:
    """
    Validate product data structure
    
    Args:
        product: Product dictionary
        
    Returns:
        True if valid, False otherwise
    """
    required_fields = ['title', 'price', 'url', 'site']
    
    # Check required fields exist
    for field in required_fields:
        if field not in product:
            return False
        if not product[field]:
            return False
    
    # Validate title
    if not isinstance(product['title'], str) or len(product['title']) < 3:
        return False
    
    # Validate price
    if product['price'] is not None:
        if not isinstance(product['price'], (int, float)):
            return False
        if product['price'] < 0:
            return False
    
    # Validate URL
    if not validate_url(product['url']):
        return False
    
    return True


def sanitize_text(text: str) -> str:
    """
    Sanitize text by removing extra whitespace and special characters
    
    Args:
        text: Text to sanitize
        
    Returns:
        Cleaned text
    """
    if not text:
        return ''
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    # Remove zero-width characters
    text = text.replace('\u200b', '').replace('\u200c', '').replace('\u200d', '')
    
    return text.strip()

