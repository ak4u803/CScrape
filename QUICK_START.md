# Quick Start Guide

Get your price comparison scraper up and running in 5 minutes!

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Test the Installation

```bash
python test_scraper.py
```

This will run basic tests to ensure everything is working correctly.

## Step 3: Try a Search

```bash
python main.py "wireless headphones" --max-results 5
```

This will search all enabled sites (Amazon, eBay, Walmart) for wireless headphones.

## Step 4: Integrate into Your App

Create a new Python file for your app:

```python
# my_price_app.py
from scrapers import ScraperManager

# Initialize the scraper
scraper = ScraperManager()

# Search for products
query = "gaming mouse"
results = scraper.search_all_sites_combined(query, max_results_per_site=10)

# Show results
print(f"Found {len(results)} products:\n")
for product in results[:5]:
    print(f"{product['title']}")
    print(f"  ${product['price']:.2f} on {product['site']}")
    print(f"  {product['url']}\n")
```

Run your app:
```bash
python my_price_app.py
```

## Step 5: Explore More Features

### Get Best Deals
```python
best_deals = scraper.get_best_deals("laptop", top_n=5)
```

### Compare Prices
```python
comparison = scraper.compare_prices("iphone")
print(f"Lowest: ${comparison['lowest_price']:.2f}")
print(f"Average: ${comparison['average_price']:.2f}")
```

### Search Specific Sites
```python
results = scraper.search_specific_sites("keyboard", sites=['amazon', 'ebay'])
```

## Common Use Cases

### 1. Find Products Under Budget
```python
from scrapers import ScraperManager

scraper = ScraperManager()
all_products = scraper.search_all_sites_combined("headphones")

# Filter by price
budget_products = [p for p in all_products if p['price'] and p['price'] <= 50.0]

print(f"Found {len(budget_products)} products under $50")
```

### 2. Price Alert System
```python
def check_price_alert(query, target_price):
    scraper = ScraperManager()
    results = scraper.search_all_sites_combined(query)
    
    deals = [p for p in results if p['price'] and p['price'] <= target_price]
    
    if deals:
        print(f"ALERT! Found {len(deals)} products at or below ${target_price}")
        for deal in deals:
            print(f"  {deal['title']} - ${deal['price']:.2f}")
    return deals

# Usage
check_price_alert("mechanical keyboard", 50.0)
```

### 3. Track Product Price
```python
def track_product(url, site):
    scraper = ScraperManager()
    product = scraper.scrape_product_url(url, site)
    
    if product:
        # Save to database or file
        print(f"Current price: ${product['price']:.2f}")
    
    return product

# Usage
product = track_product("https://www.amazon.com/dp/PRODUCT_ID", "amazon")
```

## Configuration Tips

Edit `config.yaml` to customize:

```yaml
# Increase speed (but be careful with rate limiting)
scraper:
  concurrent_requests: 10
  rate_limit_delay: 0.5

# Disable sites you don't need
sites:
  walmart:
    enabled: false
```

## Troubleshooting

**Problem: No results returned**
- Check internet connection
- Try increasing `rate_limit_delay` in config.yaml
- Sites may have changed HTML structure

**Problem: Slow performance**
- Reduce `max_results_per_site`
- Disable unused sites in config.yaml
- Check your internet speed

**Problem: Import errors**
- Make sure you're in the project directory
- Reinstall: `pip install -r requirements.txt`

## Next Steps

1. Check out `example_integration.py` for more examples
2. Read the full `README.md` for detailed documentation
3. Customize `config.yaml` for your needs
4. Add more sites by creating new scraper classes

## Need Help?

- Review the examples in `example_integration.py`
- Check the main `README.md` for full documentation
- Look at the code comments for detailed explanations

Happy scraping! 🎉

