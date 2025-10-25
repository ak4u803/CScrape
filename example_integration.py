"""
Example: How to integrate the scraper into your price comparison app
"""

from scrapers import ScraperManager
import json


def example_basic_search():
    """Example: Basic product search"""
    print("=== Example 1: Basic Search ===\n")
    
    # Initialize the scraper manager
    scraper = ScraperManager()
    
    # Search for a product
    query = "wireless headphones"
    results = scraper.search_all_sites_combined(query, max_results_per_site=5)
    
    # Display results
    print(f"Found {len(results)} products for '{query}':\n")
    for product in results[:3]:  # Show top 3
        print(f"Title: {product['title']}")
        print(f"Price: ${product['price']:.2f}")
        print(f"Site: {product['site']}")
        print(f"URL: {product['url']}\n")


def example_get_best_deals():
    """Example: Get best deals"""
    print("\n=== Example 2: Get Best Deals ===\n")
    
    scraper = ScraperManager()
    
    query = "laptop"
    best_deals = scraper.get_best_deals(query, top_n=3)
    
    print(f"Top 3 best deals for '{query}':\n")
    for i, deal in enumerate(best_deals, 1):
        print(f"{i}. {deal['title']}")
        print(f"   ${deal['price']:.2f} on {deal['site']}")
        print(f"   {deal['url']}\n")


def example_price_comparison():
    """Example: Price comparison analysis"""
    print("\n=== Example 3: Price Comparison ===\n")
    
    scraper = ScraperManager()
    
    query = "iphone"
    comparison = scraper.compare_prices(query)
    
    print(f"Price comparison for '{query}':")
    print(f"Total results: {comparison['total_results']}")
    print(f"Lowest price: ${comparison['lowest_price']:.2f}")
    print(f"Highest price: ${comparison['highest_price']:.2f}")
    print(f"Average price: ${comparison['average_price']:.2f}\n")
    
    print("Best deal:")
    best = comparison['best_deal']
    print(f"  {best['title']}")
    print(f"  ${best['price']:.2f} on {best['site']}")


def example_specific_sites():
    """Example: Search specific sites only"""
    print("\n=== Example 4: Search Specific Sites ===\n")
    
    scraper = ScraperManager()
    
    query = "gaming mouse"
    sites = ['amazon', 'ebay']  # Only search these sites
    
    results = scraper.search_specific_sites(query, sites, max_results_per_site=3)
    
    for site, products in results.items():
        print(f"\n{site.upper()} results:")
        for product in products:
            print(f"  - {product['title']} (${product['price']:.2f})")


def example_scrape_specific_url():
    """Example: Scrape a specific product URL"""
    print("\n=== Example 5: Scrape Specific URL ===\n")
    
    scraper = ScraperManager()
    
    # Example: scrape a specific Amazon product
    url = "https://www.amazon.com/dp/B08N5WRWNW"  # Example product
    site = "amazon"
    
    product = scraper.scrape_product_url(url, site)
    
    if product:
        print(f"Scraped product:")
        print(f"Title: {product['title']}")
        print(f"Price: ${product['price']:.2f}")
        print(f"Availability: {product['availability']}")
    else:
        print("Failed to scrape product")


def example_app_integration():
    """Example: Full integration into a price comparison app"""
    print("\n=== Example 6: App Integration ===\n")
    
    class PriceComparisonApp:
        """Simple example app"""
        
        def __init__(self):
            self.scraper = ScraperManager()
        
        def find_product(self, query: str, max_price: float = None):
            """Find products within budget"""
            results = self.scraper.search_all_sites_combined(query)
            
            if max_price:
                results = [p for p in results if p['price'] and p['price'] <= max_price]
            
            return results
        
        def track_price(self, url: str, site: str):
            """Track price of a specific product"""
            product = self.scraper.scrape_product_url(url, site)
            
            # In a real app, you would save this to a database
            return product
        
        def get_price_alert(self, query: str, target_price: float):
            """Check if any product is below target price"""
            results = self.scraper.search_all_sites_combined(query)
            
            alerts = [p for p in results if p['price'] and p['price'] <= target_price]
            
            return alerts
    
    # Use the app
    app = PriceComparisonApp()
    
    # Find products under $100
    print("Finding wireless earbuds under $100:")
    products = app.find_product("wireless earbuds", max_price=100.0)
    
    for product in products[:3]:
        print(f"  - {product['title']} (${product['price']:.2f}) on {product['site']}")
    
    # Check for price alerts
    print("\n\nChecking for gaming keyboards under $50:")
    alerts = app.get_price_alert("gaming keyboard", target_price=50.0)
    
    if alerts:
        print(f"Found {len(alerts)} products below target price!")
        for alert in alerts[:2]:
            print(f"  ALERT: {alert['title']} - ${alert['price']:.2f}")
    else:
        print("No products found below target price")


def example_export_results():
    """Example: Export results to JSON"""
    print("\n=== Example 7: Export Results ===\n")
    
    scraper = ScraperManager()
    
    query = "mechanical keyboard"
    results = scraper.search_all_sites_combined(query, max_results_per_site=5)
    
    # Export to JSON file
    output_file = "search_results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"Exported {len(results)} results to {output_file}")


if __name__ == '__main__':
    # Run all examples
    try:
        example_basic_search()
        example_get_best_deals()
        example_price_comparison()
        example_specific_sites()
        # example_scrape_specific_url()  # Commented out - needs real URL
        example_app_integration()
        example_export_results()
        
        print("\n" + "="*50)
        print("All examples completed successfully!")
        print("="*50)
        
    except Exception as e:
        print(f"Error running examples: {str(e)}")
        print("Note: Some examples require internet connection and may fail if sites are blocking requests")

