"""
Optional: REST API wrapper for the scraper
This allows you to integrate the scraper into web applications

Install Flask first: pip install flask flask-cors

Run with: python api_example.py
API will be available at: http://localhost:5000
"""

try:
    from flask import Flask, request, jsonify
    from flask_cors import CORS
    from scrapers import ScraperManager
    
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False
    print("Flask not installed. Install with: pip install flask flask-cors")


if FLASK_AVAILABLE:
    app = Flask(__name__)
    CORS(app)  # Enable CORS for web apps
    
    # Initialize scraper
    scraper = ScraperManager()
    
    
    @app.route('/')
    def home():
        """API documentation"""
        return jsonify({
            'name': 'Price Comparison Scraper API',
            'version': '1.0',
            'endpoints': {
                'GET /api/search': {
                    'description': 'Search all sites for products',
                    'parameters': {
                        'q': 'Search query (required)',
                        'max_results': 'Max results per site (default: 10)'
                    },
                    'example': '/api/search?q=laptop&max_results=5'
                },
                'GET /api/best-deals': {
                    'description': 'Get best deals for a query',
                    'parameters': {
                        'q': 'Search query (required)',
                        'top_n': 'Number of deals (default: 5)'
                    },
                    'example': '/api/best-deals?q=headphones&top_n=3'
                },
                'GET /api/compare': {
                    'description': 'Compare prices across sites',
                    'parameters': {
                        'q': 'Search query (required)'
                    },
                    'example': '/api/compare?q=iphone'
                },
                'GET /api/sites': {
                    'description': 'Get available sites',
                    'example': '/api/sites'
                },
                'POST /api/scrape': {
                    'description': 'Scrape a specific URL',
                    'body': {
                        'url': 'Product URL',
                        'site': 'Site name (amazon, ebay, walmart)'
                    },
                    'example': 'POST with JSON body'
                }
            }
        })
    
    
    @app.route('/api/search', methods=['GET'])
    def search():
        """Search all sites for products"""
        query = request.args.get('q')
        if not query:
            return jsonify({'error': 'Query parameter "q" is required'}), 400
        
        max_results = int(request.args.get('max_results', 10))
        
        try:
            results = scraper.search_all_sites_combined(query, max_results_per_site=max_results)
            return jsonify({
                'query': query,
                'total_results': len(results),
                'products': results
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    
    @app.route('/api/best-deals', methods=['GET'])
    def best_deals():
        """Get best deals"""
        query = request.args.get('q')
        if not query:
            return jsonify({'error': 'Query parameter "q" is required'}), 400
        
        top_n = int(request.args.get('top_n', 5))
        
        try:
            deals = scraper.get_best_deals(query, top_n=top_n)
            return jsonify({
                'query': query,
                'deals': deals
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    
    @app.route('/api/compare', methods=['GET'])
    def compare():
        """Compare prices"""
        query = request.args.get('q')
        if not query:
            return jsonify({'error': 'Query parameter "q" is required'}), 400
        
        try:
            comparison = scraper.compare_prices(query)
            return jsonify(comparison)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    
    @app.route('/api/sites', methods=['GET'])
    def get_sites():
        """Get available sites"""
        sites = scraper.get_available_sites()
        return jsonify({'sites': sites})
    
    
    @app.route('/api/scrape', methods=['POST'])
    def scrape_url():
        """Scrape a specific URL"""
        data = request.get_json()
        
        if not data or 'url' not in data or 'site' not in data:
            return jsonify({'error': 'URL and site are required'}), 400
        
        url = data['url']
        site = data['site']
        
        if site not in scraper.get_available_sites():
            return jsonify({'error': f'Site {site} not available'}), 400
        
        try:
            product = scraper.scrape_product_url(url, site)
            if product:
                return jsonify(product)
            else:
                return jsonify({'error': 'Failed to scrape product'}), 500
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    
    if __name__ == '__main__':
        print("="*50)
        print("Price Comparison Scraper API")
        print("="*50)
        print("\nAPI is running at: http://localhost:5000")
        print("\nExample requests:")
        print("  - http://localhost:5000/api/search?q=laptop")
        print("  - http://localhost:5000/api/best-deals?q=headphones&top_n=5")
        print("  - http://localhost:5000/api/compare?q=iphone")
        print("  - http://localhost:5000/api/sites")
        print("\n" + "="*50 + "\n")
        
        app.run(debug=True, port=5000)

else:
    print("\nTo use the API, install Flask:")
    print("  pip install flask flask-cors")
    print("\nThen run:")
    print("  python api_example.py")

