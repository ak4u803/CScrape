"""
Price parsing utilities
"""

import re
from typing import Optional, Tuple
from decimal import Decimal, InvalidOperation


def parse_price(price_text: str) -> Optional[float]:
    """
    Parse price from text string
    
    Args:
        price_text: Text containing price (e.g., "$19.99", "19,99 €", "1,299.00")
        
    Returns:
        Float price or None if parsing fails
    """
    if not price_text:
        return None
    
    try:
        # Remove common currency symbols and text
        cleaned = price_text.strip()
        
        # Remove currency symbols
        cleaned = re.sub(r'[$€£¥₹₽¢]', '', cleaned)
        
        # Remove common text
        cleaned = re.sub(r'(USD|EUR|GBP|INR|Price|From|Starting at|Sale|Now)', '', cleaned, flags=re.IGNORECASE)
        
        # Extract number patterns (handles 1,299.99 or 1.299,99 formats)
        # First, try to find the full price pattern
        patterns = [
            r'(\d{1,3}(?:,\d{3})*(?:\.\d{2}))',  # US format: 1,299.99
            r'(\d{1,3}(?:\.\d{3})*(?:,\d{2}))',  # EU format: 1.299,99
            r'(\d+\.\d{2})',                      # Simple decimal: 19.99
            r'(\d+,\d{2})',                       # Simple comma: 19,99
            r'(\d+)'                               # Just integer: 19
        ]
        
        for pattern in patterns:
            match = re.search(pattern, cleaned)
            if match:
                price_str = match.group(1)
                
                # Determine format and normalize
                if ',' in price_str and '.' in price_str:
                    # Has both - determine which is thousands separator
                    if price_str.rindex(',') > price_str.rindex('.'):
                        # EU format: 1.299,99
                        price_str = price_str.replace('.', '').replace(',', '.')
                    else:
                        # US format: 1,299.99
                        price_str = price_str.replace(',', '')
                elif ',' in price_str:
                    # Check if comma is thousands or decimal separator
                    comma_pos = price_str.rindex(',')
                    if len(price_str) - comma_pos == 3:  # Likely decimal
                        price_str = price_str.replace(',', '.')
                    else:  # Likely thousands separator
                        price_str = price_str.replace(',', '')
                
                # Convert to float
                return float(price_str)
        
        return None
    
    except (ValueError, InvalidOperation, AttributeError) as e:
        return None


def extract_currency(price_text: str) -> str:
    """
    Extract currency code from price text
    
    Args:
        price_text: Text containing price
        
    Returns:
        Currency code (USD, EUR, etc.) or 'USD' as default
    """
    if not price_text:
        return 'USD'
    
    currency_symbols = {
        '$': 'USD',
        '€': 'EUR',
        '£': 'GBP',
        '¥': 'JPY',
        '₹': 'INR',
        '₽': 'RUB',
        '¢': 'USD'
    }
    
    # Check for symbols
    for symbol, code in currency_symbols.items():
        if symbol in price_text:
            return code
    
    # Check for currency codes
    currency_codes = ['USD', 'EUR', 'GBP', 'JPY', 'INR', 'RUB', 'AUD', 'CAD']
    for code in currency_codes:
        if code.upper() in price_text.upper():
            return code
    
    return 'USD'  # Default


def format_price(price: float, currency: str = 'USD') -> str:
    """
    Format price for display
    
    Args:
        price: Price value
        currency: Currency code
        
    Returns:
        Formatted price string
    """
    currency_symbols = {
        'USD': '$',
        'EUR': '€',
        'GBP': '£',
        'JPY': '¥',
        'INR': '₹',
        'RUB': '₽'
    }
    
    symbol = currency_symbols.get(currency, '$')
    return f"{symbol}{price:.2f}"

