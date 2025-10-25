"""
Main entry point for the web scraper
Simple command-line interface for testing
"""

import argparse
import json
from scrapers import ScraperManager


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Price Comparison Web Scraper')
    parser.add_argument('query', type=str, help='Product search query')
    parser.add_argument('--max-results', type=int, default=10, help='Maximum results per site')
    parser.add_argument('--sites', nargs='+', help='Specific sites to search (amazon, ebay, walmart)')
    parser.add_argument('--best-deals', action='store_true', help='Show only best deals')
    parser.add_argument('--compare', action='store_true', help='Show price comparison analysis')
    parser.add_argument('--output', type=str, help='Output file (JSON format)')
    
    args = parser.parse_args()
    
    # Initialize scraper manager
    print(f"Initializing scraper...")
    manager = ScraperManager()
    
    print(f"Available sites: {', '.join(manager.get_available_sites())}\n")
    
    # Perform search
    if args.best_deals:
        print(f"Searching for best deals on: {args.query}")
        results = manager.get_best_deals(args.query, top_n=5)
        
        print(f"\n=== Top 5 Best Deals ===\n")
        for i, product in enumerate(results, 1):
            print(f"{i}. {product['title']}")
            print(f"   Price: ${product['price']:.2f}")
            print(f"   Site: {product['site']}")
            print(f"   URL: {product['url']}")
            print()
    
    elif args.compare:
        print(f"Comparing prices for: {args.query}")
        analysis = manager.compare_prices(args.query)
        
        print(f"\n=== Price Comparison Analysis ===\n")
        print(f"Total Results: {analysis['total_results']}")
        if analysis['lowest_price']:
            print(f"Lowest Price: ${analysis['lowest_price']:.2f}")
            print(f"Highest Price: ${analysis['highest_price']:.2f}")
            print(f"Average Price: ${analysis['average_price']:.2f}")
            print(f"\nBest Deal:")
            best = analysis['best_deal']
            print(f"  {best['title']}")
            print(f"  ${best['price']:.2f} on {best['site']}")
            print(f"  {best['url']}")
        
        results = analysis
    
    elif args.sites:
        print(f"Searching {', '.join(args.sites)} for: {args.query}")
        results = manager.search_specific_sites(args.query, args.sites, args.max_results)
        
        for site, products in results.items():
            print(f"\n=== {site.upper()} ({len(products)} results) ===\n")
            for i, product in enumerate(products, 1):
                print(f"{i}. {product['title']}")
                if product['price']:
                    print(f"   Price: ${product['price']:.2f}")
                print(f"   URL: {product['url'][:80]}...")
                print()
    
    else:
        print(f"Searching all sites for: {args.query}")
        results = manager.search_all_sites_combined(args.query, args.max_results)
        
        print(f"\n=== Combined Results ({len(results)} products, sorted by price) ===\n")
        for i, product in enumerate(results, 1):
            print(f"{i}. {product['title']}")
            if product['price']:
                print(f"   Price: ${product['price']:.2f}")
            print(f"   Site: {product['site']}")
            print(f"   URL: {product['url'][:80]}...")
            print()
    
    # Save to file if requested
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, default=str)
        print(f"\nResults saved to {args.output}")


if __name__ == '__main__':
    main()

