"""
AliExpress-specific scraper implementation
"""

from typing import Dict, List, Optional, Any
from urllib.parse import quote_plus
from .base_scraper import BaseScraper


class AliExpressScraper(BaseScraper):
    """
    Scraper for AliExpress.com
    """
    
    @property
    def site_name(self) -> str:
        return 'aliexpress'
    
    def scrape_product(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Scrape a single AliExpress product page
        
        Args:
            url: Product page URL
            
        Returns:
            Product data dictionary or None
        """
        self.logger.info(f"Scraping AliExpress product: {url}")
        
        html = self._fetch_page(url)
        if not html:
            return None
        
        soup = self._parse_html(html)
        
        # Extract product data
        title = self._extract_text(soup, self.selectors['title'])
        price_text = self._extract_text(soup, self.selectors['price'])
        image_url = self._extract_attribute(soup, self.selectors['image'], 'src')
        availability = self._extract_text(soup, self.selectors['availability'])
        
        product_data = self.format_product_data(
            title=title,
            price=price_text,
            url=url,
            image_url=image_url,
            availability=availability if availability else 'Available'
        )
        
        if product_data:
            self.logger.info(f"Successfully scraped: {title}")
        
        return product_data
    
    def search_products(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """
        Search AliExpress for products
        
        Args:
            query: Search query
            max_results: Maximum number of results
            
        Returns:
            List of product dictionaries
        """
        self.logger.info(f"Searching AliExpress for: {query}")
        
        search_url = self.site_config['search_url'].format(query=quote_plus(query))
        html = self._fetch_page(search_url)
        
        if not html:
            return []
        
        soup = self._parse_html(html)
        products = []
        
        # Find product containers
        product_items = soup.select('[data-product-id], .list-item')
        
        for item in product_items[:max_results]:
            try:
                # Extract title and URL
                title_elem = item.select_one('a[title], .title a, h1')
                if not title_elem:
                    continue
                
                # Try to get title from title attribute first
                title = title_elem.get('title', '')
                if not title:
                    title = title_elem.get_text(strip=True)
                
                product_url = title_elem.get('href', '')
                if not product_url:
                    url_elem = item.select_one('a')
                    product_url = url_elem.get('href', '') if url_elem else ''
                
                # Make URL absolute
                if product_url and not product_url.startswith('http'):
                    if product_url.startswith('//'):
                        product_url = f"https:{product_url}"
                    elif product_url.startswith('/'):
                        product_url = f"https://www.aliexpress.com{product_url}"
                
                # Extract price
                price_elem = item.select_one('.price-current, .mGXnE_item, [class*="price"]')
                price_text = price_elem.get_text(strip=True) if price_elem else None
                
                # Extract image
                img_elem = item.select_one('img')
                image_url = img_elem.get('src', '') if img_elem else ''
                
                # Handle data-src attribute
                if not image_url and img_elem:
                    image_url = img_elem.get('data-src', '')
                
                product_data = self.format_product_data(
                    title=title,
                    price=price_text if price_text else '0',
                    url=product_url,
                    image_url=image_url,
                    availability='Available'
                )
                
                if product_data:
                    products.append(product_data)
                
            except Exception as e:
                self.logger.error(f"Error parsing AliExpress search result: {str(e)}")
                continue
        
        self.logger.info(f"Found {len(products)} products on AliExpress")
        return products

