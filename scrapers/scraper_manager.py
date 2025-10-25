"""
Scraper Manager - Main orchestrator for all scrapers
This is the primary interface for integrating the scraper into your app
"""

import logging
from typing import Dict, List, Optional, Any
from concurrent.futures import ThreadPoolExecutor, as_completed

from .amazon_scraper import AmazonScraper
from .ebay_scraper import EbayScraper
from .walmart_scraper import WalmartScraper
from .target_scraper import TargetScraper
from .bestbuy_scraper import BestBuyScraper
from .newegg_scraper import NeweggScraper
from .etsy_scraper import EtsyScraper
from .aliexpress_scraper import AliExpressScraper
from utils.config_loader import load_config, get_enabled_sites


class ScraperManager:
    """
    Main manager class to orchestrate all site-specific scrapers
    This is the primary interface for your price comparison app
    """
    
    def __init__(self, config_path: str = 'config.yaml'):
        """
        Initialize the scraper manager
        
        Args:
            config_path: Path to configuration file
        """
        self.config = load_config(config_path)
        self.scrapers = {}
        self._setup_logging()
        self._initialize_scrapers()
    
    def _setup_logging(self):
        """Setup logging configuration"""
        log_config = self.config.get('logging', {})
        level = getattr(logging, log_config.get('level', 'INFO'))
        
        # Setup root logger
        logging.basicConfig(
            level=level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_config.get('file', 'scraper.log')),
                logging.StreamHandler() if log_config.get('console', True) else logging.NullHandler()
            ]
        )
        
        self.logger = logging.getLogger('scraper.manager')
    
    def _initialize_scrapers(self):
        """Initialize all enabled scrapers"""
        enabled_sites = get_enabled_sites(self.config)
        
        scraper_classes = {
            'amazon': AmazonScraper,
            'ebay': EbayScraper,
            'walmart': WalmartScraper,
            'target': TargetScraper,
            'bestbuy': BestBuyScraper,
            'newegg': NeweggScraper,
            'etsy': EtsyScraper,
            'aliexpress': AliExpressScraper
        }
        
        for site in enabled_sites:
            if site in scraper_classes:
                try:
                    self.scrapers[site] = scraper_classes[site](self.config)
                    self.logger.info(f"Initialized {site} scraper")
                except Exception as e:
                    self.logger.error(f"Failed to initialize {site} scraper: {str(e)}")
        
        self.logger.info(f"Initialized {len(self.scrapers)} scrapers")
    
    def search_all_sites(self, query: str, max_results_per_site: int = 10) -> Dict[str, List[Dict[str, Any]]]:
        """
        Search all enabled sites for a product
        
        Args:
            query: Search query
            max_results_per_site: Maximum results per site
            
        Returns:
            Dictionary with site names as keys and product lists as values
        """
        self.logger.info(f"Searching all sites for: {query}")
        results = {}
        
        max_workers = self.config.get('scraper', {}).get('concurrent_requests', 5)
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all scraping tasks
            future_to_site = {
                executor.submit(scraper.search_products, query, max_results_per_site): site
                for site, scraper in self.scrapers.items()
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_site):
                site = future_to_site[future]
                try:
                    results[site] = future.result()
                except Exception as e:
                    self.logger.error(f"Error searching {site}: {str(e)}")
                    results[site] = []
        
        return results
    
    def search_all_sites_combined(self, query: str, max_results_per_site: int = 10) -> List[Dict[str, Any]]:
        """
        Search all enabled sites and return combined results sorted by price
        
        Args:
            query: Search query
            max_results_per_site: Maximum results per site
            
        Returns:
            Combined list of products sorted by price (lowest first)
        """
        results = self.search_all_sites(query, max_results_per_site)
        
        # Combine all results
        combined = []
        for site, products in results.items():
            combined.extend(products)
        
        # Sort by price (lowest first), handling None prices
        combined.sort(key=lambda x: x['price'] if x['price'] is not None else float('inf'))
        
        self.logger.info(f"Found {len(combined)} total products across all sites")
        return combined
    
    def search_specific_sites(self, query: str, sites: List[str], max_results_per_site: int = 10) -> Dict[str, List[Dict[str, Any]]]:
        """
        Search specific sites for a product
        
        Args:
            query: Search query
            sites: List of site names to search
            max_results_per_site: Maximum results per site
            
        Returns:
            Dictionary with site names as keys and product lists as values
        """
        self.logger.info(f"Searching {', '.join(sites)} for: {query}")
        results = {}
        
        max_workers = self.config.get('scraper', {}).get('concurrent_requests', 5)
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit tasks only for requested sites
            future_to_site = {
                executor.submit(self.scrapers[site].search_products, query, max_results_per_site): site
                for site in sites if site in self.scrapers
            }
            
            # Collect results
            for future in as_completed(future_to_site):
                site = future_to_site[future]
                try:
                    results[site] = future.result()
                except Exception as e:
                    self.logger.error(f"Error searching {site}: {str(e)}")
                    results[site] = []
        
        return results
    
    def scrape_product_url(self, url: str, site: str) -> Optional[Dict[str, Any]]:
        """
        Scrape a specific product URL
        
        Args:
            url: Product URL
            site: Site name (amazon, ebay, walmart)
            
        Returns:
            Product data dictionary or None
        """
        if site not in self.scrapers:
            self.logger.error(f"Scraper for {site} not available")
            return None
        
        return self.scrapers[site].scrape_product(url)
    
    def get_best_deals(self, query: str, top_n: int = 5) -> List[Dict[str, Any]]:
        """
        Get the best deals (lowest prices) for a query
        
        Args:
            query: Search query
            top_n: Number of top deals to return
            
        Returns:
            List of top N cheapest products
        """
        all_products = self.search_all_sites_combined(query)
        
        # Filter out products without prices
        valid_products = [p for p in all_products if p['price'] is not None and p['price'] > 0]
        
        return valid_products[:top_n]
    
    def compare_prices(self, query: str) -> Dict[str, Any]:
        """
        Compare prices across all sites and provide analysis
        
        Args:
            query: Search query
            
        Returns:
            Dictionary with price comparison data
        """
        results = self.search_all_sites_combined(query)
        
        if not results:
            return {
                'query': query,
                'total_results': 0,
                'lowest_price': None,
                'highest_price': None,
                'average_price': None,
                'products': []
            }
        
        # Filter valid prices
        valid_prices = [p['price'] for p in results if p['price'] is not None and p['price'] > 0]
        
        return {
            'query': query,
            'total_results': len(results),
            'lowest_price': min(valid_prices) if valid_prices else None,
            'highest_price': max(valid_prices) if valid_prices else None,
            'average_price': sum(valid_prices) / len(valid_prices) if valid_prices else None,
            'best_deal': results[0] if results else None,
            'products': results
        }
    
    def get_available_sites(self) -> List[str]:
        """
        Get list of available/enabled sites
        
        Returns:
            List of site names
        """
        return list(self.scrapers.keys())

