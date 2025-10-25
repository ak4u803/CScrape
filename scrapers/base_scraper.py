"""
Base Scraper Class
All site-specific scrapers inherit from this class
"""

import requests
import time
import logging
from bs4 import BeautifulSoup
from typing import Dict, List, Optional, Any
from abc import ABC, abstractmethod
from tenacity import retry, stop_after_attempt, wait_exponential
from fake_useragent import UserAgent

from utils.price_parser import parse_price
from utils.validators import validate_url, validate_product_data


class BaseScraper(ABC):
    """
    Abstract base class for all web scrapers
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the base scraper
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.scraper_config = config.get('scraper', {})
        self.site_config = config.get('sites', {}).get(self.site_name, {})
        self.selectors = self.site_config.get('selectors', {})
        
        # Setup session
        self.session = requests.Session()
        self.ua = UserAgent()
        self._setup_session()
        
        # Setup logging
        self.logger = logging.getLogger(f"scraper.{self.site_name}")
        self._setup_logging()
        
        # Rate limiting
        self.last_request_time = 0
        self.rate_limit_delay = self.scraper_config.get('rate_limit_delay', 1)
        
    def _setup_session(self):
        """Configure the requests session"""
        user_agent = self.scraper_config.get('user_agent', self.ua.random)
        self.session.headers.update({
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
    
    def _setup_logging(self):
        """Setup logging configuration"""
        log_config = self.config.get('logging', {})
        level = getattr(logging, log_config.get('level', 'INFO'))
        self.logger.setLevel(level)
    
    def _rate_limit(self):
        """Implement rate limiting between requests"""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.rate_limit_delay:
            time.sleep(self.rate_limit_delay - elapsed)
        self.last_request_time = time.time()
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def _fetch_page(self, url: str) -> Optional[str]:
        """
        Fetch a webpage with retry logic
        
        Args:
            url: URL to fetch
            
        Returns:
            HTML content as string or None if failed
        """
        if not validate_url(url):
            self.logger.error(f"Invalid URL: {url}")
            return None
        
        self._rate_limit()
        
        try:
            timeout = self.scraper_config.get('timeout', 10)
            response = self.session.get(url, timeout=timeout)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error fetching {url}: {str(e)}")
            raise
    
    def _parse_html(self, html: str) -> BeautifulSoup:
        """
        Parse HTML content
        
        Args:
            html: HTML string
            
        Returns:
            BeautifulSoup object
        """
        return BeautifulSoup(html, 'lxml')
    
    def _extract_text(self, soup: BeautifulSoup, selector: str) -> Optional[str]:
        """
        Extract text from HTML using CSS selector
        
        Args:
            soup: BeautifulSoup object
            selector: CSS selector
            
        Returns:
            Extracted text or None
        """
        try:
            # Handle multiple selectors separated by comma
            selectors = [s.strip() for s in selector.split(',')]
            for sel in selectors:
                element = soup.select_one(sel)
                if element:
                    return element.get_text(strip=True)
            return None
        except Exception as e:
            self.logger.error(f"Error extracting text with selector '{selector}': {str(e)}")
            return None
    
    def _extract_attribute(self, soup: BeautifulSoup, selector: str, attribute: str) -> Optional[str]:
        """
        Extract attribute from HTML element
        
        Args:
            soup: BeautifulSoup object
            selector: CSS selector
            attribute: Attribute name
            
        Returns:
            Attribute value or None
        """
        try:
            selectors = [s.strip() for s in selector.split(',')]
            for sel in selectors:
                element = soup.select_one(sel)
                if element and element.has_attr(attribute):
                    return element[attribute]
            return None
        except Exception as e:
            self.logger.error(f"Error extracting attribute '{attribute}': {str(e)}")
            return None
    
    @abstractmethod
    def site_name(self) -> str:
        """Return the name of the site this scraper handles"""
        pass
    
    @abstractmethod
    def scrape_product(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Scrape a single product page
        
        Args:
            url: Product page URL
            
        Returns:
            Dictionary containing product data or None
        """
        pass
    
    @abstractmethod
    def search_products(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """
        Search for products and return results
        
        Args:
            query: Search query
            max_results: Maximum number of results to return
            
        Returns:
            List of product dictionaries
        """
        pass
    
    def format_product_data(self, **kwargs) -> Dict[str, Any]:
        """
        Format scraped data into a standard structure
        
        Args:
            **kwargs: Product fields
            
        Returns:
            Formatted product dictionary
        """
        product = {
            'title': kwargs.get('title', ''),
            'price': parse_price(kwargs.get('price', '')),
            'currency': kwargs.get('currency', 'USD'),
            'url': kwargs.get('url', ''),
            'image_url': kwargs.get('image_url', ''),
            'availability': kwargs.get('availability', 'Unknown'),
            'site': self.site_name,
            'scraped_at': time.time()
        }
        
        # Validate the data
        if validate_product_data(product):
            return product
        else:
            self.logger.warning(f"Invalid product data: {product}")
            return None

