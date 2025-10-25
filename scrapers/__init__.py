"""
Web Scraper Package for Price Comparison
"""

from .base_scraper import BaseScraper
from .amazon_scraper import AmazonScraper
from .ebay_scraper import EbayScraper
from .walmart_scraper import WalmartScraper
from .target_scraper import TargetScraper
from .bestbuy_scraper import BestBuyScraper
from .newegg_scraper import NeweggScraper
from .etsy_scraper import EtsyScraper
from .aliexpress_scraper import AliExpressScraper
from .scraper_manager import ScraperManager

__all__ = [
    'BaseScraper',
    'AmazonScraper',
    'EbayScraper', 
    'WalmartScraper',
    'TargetScraper',
    'BestBuyScraper',
    'NeweggScraper',
    'EtsyScraper',
    'AliExpressScraper',
    'ScraperManager'
]

