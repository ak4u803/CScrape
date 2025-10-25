"""
eBay-specific scraper implementation
"""

from typing import Dict, List, Optional, Any
from urllib.parse import quote_plus
from .base_scraper import BaseScraper


class EbayScraper(BaseScraper):
    """
    Scraper for eBay.com
    """
    
    @property
    def site_name(self) -> str:
        return 'ebay'
    
    def scrape_product(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Scrape a single eBay product page
        
        Args:
            url: Product page URL
            
        Returns:
            Product data dictionary or None
        """
        self.logger.info(f"Scraping eBay product: {url}")
        
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
        Search eBay for products
        
        Args:
            query: Search query
            max_results: Maximum number of results
            
        Returns:
            List of product dictionaries
        """
        self.logger.info(f"Searching eBay for: {query}")
        
        search_url = self.site_config['search_url'].format(query=quote_plus(query))
        html = self._fetch_page(search_url)
        
        if not html:
            return []
        
        soup = self._parse_html(html)
        products = []
        
        # Find product containers
        product_items = soup.select('.s-item, .lvresult')
        
        for item in product_items[:max_results]:
            try:
                # Skip sponsored/ad items
                if item.select_one('.s-item__title--tag'):
                    continue
                
                # Extract title and URL
                title_elem = item.select_one('.s-item__title, .lvtitle a')
                if not title_elem:
                    continue
                
                # Get title
                if title_elem.name == 'a':
                    title = title_elem.get_text(strip=True)
                    product_url = title_elem.get('href', '')
                else:
                    title = title_elem.get_text(strip=True)
                    url_elem = item.select_one('.s-item__link, a.s-item__link')
                    product_url = url_elem.get('href', '') if url_elem else ''
                
                # Skip placeholder items
                if 'Shop on eBay' in title:
                    continue
                
                # Extract price
                price_elem = item.select_one('.s-item__price, .lvprice .prc')
                price_text = price_elem.get_text(strip=True) if price_elem else None
                
                # Extract image
                img_elem = item.select_one('.s-item__image-img, img.img')
                image_url = img_elem.get('src', '') if img_elem else ''
                
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
                self.logger.error(f"Error parsing eBay search result: {str(e)}")
                continue
        
        self.logger.info(f"Found {len(products)} products on eBay")
        return products

