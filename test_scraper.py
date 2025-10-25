"""
Simple tests for the scraper
Run with: python test_scraper.py
"""

from scrapers import ScraperManager
from utils.price_parser import parse_price, extract_currency
from utils.validators import validate_url, validate_product_data


def test_price_parser():
    """Test price parsing"""
    print("Testing price parser...")
    
    test_cases = [
        ("$19.99", 19.99),
        ("1,299.00", 1299.00),
        ("€29.95", 29.95),
        ("Price: $99", 99.0),
        ("From $49.99", 49.99),
    ]
    
    for price_text, expected in test_cases:
        result = parse_price(price_text)
        if result == expected:
            print(f"  ✓ '{price_text}' -> {result}")
        else:
            print(f"  ✗ '{price_text}' -> {result} (expected {expected})")


def test_currency_extraction():
    """Test currency extraction"""
    print("\nTesting currency extraction...")
    
    test_cases = [
        ("$19.99", "USD"),
        ("€29.95", "EUR"),
        ("£39.99", "GBP"),
    ]
    
    for price_text, expected in test_cases:
        result = extract_currency(price_text)
        if result == expected:
            print(f"  ✓ '{price_text}' -> {result}")
        else:
            print(f"  ✗ '{price_text}' -> {result} (expected {expected})")


def test_url_validator():
    """Test URL validation"""
    print("\nTesting URL validator...")
    
    test_cases = [
        ("https://www.amazon.com/product", True),
        ("http://ebay.com", True),
        ("not a url", False),
        ("", False),
    ]
    
    for url, expected in test_cases:
        result = validate_url(url)
        if result == expected:
            print(f"  ✓ '{url}' -> {result}")
        else:
            print(f"  ✗ '{url}' -> {result} (expected {expected})")


def test_product_validator():
    """Test product data validation"""
    print("\nTesting product validator...")
    
    valid_product = {
        'title': 'Test Product',
        'price': 99.99,
        'url': 'https://example.com/product',
        'site': 'amazon'
    }
    
    invalid_product = {
        'title': 'Test',
        'price': -10,  # Invalid negative price
        'url': 'not a url',
        'site': 'test'
    }
    
    if validate_product_data(valid_product):
        print("  ✓ Valid product passed")
    else:
        print("  ✗ Valid product failed")
    
    if not validate_product_data(invalid_product):
        print("  ✓ Invalid product rejected")
    else:
        print("  ✗ Invalid product accepted")


def test_scraper_initialization():
    """Test scraper initialization"""
    print("\nTesting scraper initialization...")
    
    try:
        scraper = ScraperManager()
        sites = scraper.get_available_sites()
        print(f"  ✓ Scraper initialized with sites: {', '.join(sites)}")
    except Exception as e:
        print(f"  ✗ Scraper initialization failed: {str(e)}")


def test_live_search():
    """Test live search (optional - requires internet)"""
    print("\nTesting live search (optional)...")
    print("  Note: This test requires internet connection and may take a while")
    
    response = input("  Run live search test? (y/n): ").lower().strip()
    
    if response == 'y':
        try:
            scraper = ScraperManager()
            print("  Searching for 'test product'...")
            results = scraper.search_all_sites_combined("test product", max_results_per_site=2)
            
            if results:
                print(f"  ✓ Found {len(results)} products")
                print(f"  Sample: {results[0]['title'][:50]}...")
            else:
                print("  ⚠ No results found (may be normal)")
        except Exception as e:
            print(f"  ✗ Live search failed: {str(e)}")
    else:
        print("  ⊘ Live search test skipped")


def main():
    """Run all tests"""
    print("="*50)
    print("Running Scraper Tests")
    print("="*50 + "\n")
    
    test_price_parser()
    test_currency_extraction()
    test_url_validator()
    test_product_validator()
    test_scraper_initialization()
    test_live_search()
    
    print("\n" + "="*50)
    print("Tests completed!")
    print("="*50)


if __name__ == '__main__':
    main()

