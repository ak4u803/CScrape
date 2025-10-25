# Custom Web Scraper for Price Comparison

A powerful, modular web scraper designed for price comparison applications. Easily scrape product information from multiple e-commerce sites and find the best deals.

## Features

- 🚀 **Multi-Site Support**: Built-in scrapers for Amazon, eBay, and Walmart
- ⚡ **Concurrent Scraping**: Fast parallel requests across multiple sites
- 🔧 **Easy Configuration**: YAML-based configuration for easy customization
- 🛡️ **Robust**: Retry logic, rate limiting, and error handling
- 📊 **Price Analysis**: Compare prices, find best deals, calculate averages
- 🔌 **Easy Integration**: Simple API for integrating into your app
- 📝 **Logging**: Comprehensive logging for debugging and monitoring

## Installation

1. Clone or download this repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Quick Start

### Command Line Usage

```bash
# Search all sites for a product
python main.py "wireless headphones"

# Get best deals
python main.py "laptop" --best-deals

# Compare prices with analysis
python main.py "gaming mouse" --compare

# Search specific sites only
python main.py "iphone" --sites amazon ebay

# Save results to JSON
python main.py "mechanical keyboard" --output results.json
```

### Python API Usage

```python
from scrapers import ScraperManager

# Initialize the scraper
scraper = ScraperManager()

# Search all sites
results = scraper.search_all_sites_combined("wireless headphones")

# Get best deals
best_deals = scraper.get_best_deals("laptop", top_n=5)

# Compare prices
comparison = scraper.compare_prices("gaming mouse")

print(f"Lowest price: ${comparison['lowest_price']:.2f}")
print(f"Best deal: {comparison['best_deal']['title']}")
```

## Integration into Your App

### Example 1: Simple Integration

```python
from scrapers import ScraperManager

class YourPriceComparisonApp:
    def __init__(self):
        self.scraper = ScraperManager()
    
    def search_products(self, query):
        # Get all products sorted by price
        return self.scraper.search_all_sites_combined(query)
    
    def get_cheapest(self, query):
        # Get the cheapest products
        return self.scraper.get_best_deals(query, top_n=5)

# Use in your app
app = YourPriceComparisonApp()
products = app.search_products("wireless earbuds")
```

### Example 2: Advanced Integration with Filtering

```python
from scrapers import ScraperManager

class AdvancedPriceApp:
    def __init__(self):
        self.scraper = ScraperManager()
    
    def find_products_under_budget(self, query, max_price):
        """Find products within budget"""
        results = self.scraper.search_all_sites_combined(query)
        return [p for p in results if p['price'] and p['price'] <= max_price]
    
    def price_alert(self, query, target_price):
        """Check if any product is below target price"""
        results = self.scraper.search_all_sites_combined(query)
        alerts = [p for p in results if p['price'] and p['price'] <= target_price]
        return alerts
    
    def track_product(self, url, site):
        """Track a specific product"""
        return self.scraper.scrape_product_url(url, site)

# Use in your app
app = AdvancedPriceApp()

# Find products under $100
products = app.find_products_under_budget("headphones", 100.0)

# Set price alert
alerts = app.price_alert("gaming keyboard", 50.0)
if alerts:
    print(f"Found {len(alerts)} products below target price!")
```

## Configuration

Edit `config.yaml` to customize the scraper:

```yaml
scraper:
  timeout: 10  # Request timeout in seconds
  max_retries: 3  # Number of retries for failed requests
  rate_limit_delay: 1  # Delay between requests (seconds)
  concurrent_requests: 5  # Number of concurrent requests

sites:
  amazon:
    enabled: true
    # Add custom selectors if needed
  
  ebay:
    enabled: true
  
  walmart:
    enabled: false  # Disable sites you don't need
```

## API Reference

### ScraperManager

Main class for interacting with the scraper.

#### Methods

**`search_all_sites_combined(query, max_results_per_site=10)`**
- Search all enabled sites and return combined results sorted by price
- Returns: List of product dictionaries

**`get_best_deals(query, top_n=5)`**
- Get the N cheapest products
- Returns: List of top N products

**`compare_prices(query)`**
- Compare prices across all sites with analysis
- Returns: Dictionary with price statistics and products

**`search_specific_sites(query, sites, max_results_per_site=10)`**
- Search only specific sites
- Args: `sites` - list of site names ['amazon', 'ebay', 'walmart']
- Returns: Dictionary with site names as keys

**`scrape_product_url(url, site)`**
- Scrape a specific product URL
- Args: `url` - product URL, `site` - site name
- Returns: Product dictionary

**`get_available_sites()`**
- Get list of enabled sites
- Returns: List of site names

### Product Data Structure

Each product is returned as a dictionary with the following structure:

```python
{
    'title': 'Product Name',
    'price': 99.99,  # float or None
    'currency': 'USD',
    'url': 'https://...',
    'image_url': 'https://...',
    'availability': 'In Stock',
    'site': 'amazon',
    'scraped_at': 1234567890.0  # Unix timestamp
}
```

## Adding New Sites

To add support for a new site:

1. Create a new scraper class in `scrapers/` (e.g., `target_scraper.py`)
2. Inherit from `BaseScraper`
3. Implement required methods:
   - `site_name` property
   - `scrape_product(url)` method
   - `search_products(query, max_results)` method

```python
from .base_scraper import BaseScraper

class TargetScraper(BaseScraper):
    @property
    def site_name(self) -> str:
        return 'target'
    
    def scrape_product(self, url):
        # Implementation
        pass
    
    def search_products(self, query, max_results=10):
        # Implementation
        pass
```

4. Add the site configuration to `config.yaml`
5. Register the scraper in `scrapers/scraper_manager.py`

## Best Practices

1. **Rate Limiting**: The scraper includes built-in rate limiting. Adjust `rate_limit_delay` in config if needed.

2. **Error Handling**: The scraper handles errors gracefully. Check logs for debugging.

3. **Respect robots.txt**: Set `respect_robots_txt: true` in config to be respectful.

4. **User Agents**: The scraper rotates user agents to avoid detection. Customize in config if needed.

5. **Caching**: Consider implementing caching in your app to reduce requests.

6. **Legal Considerations**: Ensure you comply with each site's Terms of Service and local laws regarding web scraping.

## Troubleshooting

### No results returned

- Check your internet connection
- Sites may have changed their HTML structure (update selectors in config)
- You may be rate-limited (increase `rate_limit_delay`)

### Import errors

- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Ensure you're running from the project root directory

### Slow performance

- Reduce `max_results_per_site`
- Disable sites you don't need in config
- Increase `concurrent_requests` (but be careful with rate limiting)

## Examples

See `example_integration.py` for comprehensive examples including:
- Basic searching
- Finding best deals
- Price comparison
- Searching specific sites
- Full app integration
- Exporting results

Run examples:
```bash
python example_integration.py
```

## Project Structure

```
ScraperV1/
├── config.yaml              # Configuration file
├── requirements.txt         # Python dependencies
├── main.py                 # Command-line interface
├── example_integration.py  # Integration examples
├── scrapers/
│   ├── __init__.py
│   ├── base_scraper.py     # Base scraper class
│   ├── amazon_scraper.py   # Amazon scraper
│   ├── ebay_scraper.py     # eBay scraper
│   ├── walmart_scraper.py  # Walmart scraper
│   └── scraper_manager.py  # Main orchestrator
└── utils/
    ├── __init__.py
    ├── price_parser.py     # Price parsing utilities
    ├── validators.py       # Data validation
    └── config_loader.py    # Config loading
```

## License

This project is provided as-is for educational and personal use. Please ensure you comply with all applicable laws and website Terms of Service when using this scraper.

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the example code in `example_integration.py`
3. Check the logs in `scraper.log`

## Future Enhancements

Potential improvements you could add:
- Database integration for storing historical prices
- Price tracking and alerts
- More e-commerce sites (Best Buy, Target, etc.)
- Proxy rotation for large-scale scraping
- Selenium integration for JavaScript-heavy sites
- API endpoint wrapper (Flask/FastAPI)
- Caching layer (Redis)
- Product image download
- Price history graphs

---

Happy scraping! 🚀

