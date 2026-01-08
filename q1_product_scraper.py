import requests
from bs4 import BeautifulSoup
import json
import urllib.parse

def search_mdcomputers(search_term):
    # Base URL for the search query
    base_url = "https://mdcomputers.in/index.php"
    
    # Construct the query parameters
    params = {
        "route": "product/search",
        "search": search_term
    }
    
    # Mock User-Agent to prevent 403/blocking
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        # Fetch the content
        response = requests.get(base_url, params=params, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        products = []
        
        # OpenCart themes usually use .product-layout or .product-thumb for item containers
        # Inspecting standard structure for mdcomputers:
        product_items = soup.select('.product-thumb')
        
        if not product_items:
            # Fallback for list view specific layouts if grid isn't default
            product_items = soup.select('.product-list > div')

        for item in product_items:
            product_data = {}
            
            # Extract Name
            name_tag = item.select_one('.caption h4 a')
            if name_tag:
                product_data['name'] = name_tag.get_text(strip=True)
                product_data['url'] = name_tag['href']
            else:
                continue # Skip if no name found

            # Extract Price
            price_tag = item.select_one('.price')
            if price_tag:
                # Handle sales prices (New vs Old)
                price_new = price_tag.select_one('.price-new')
                if price_new:
                    product_data['price'] = price_new.get_text(strip=True)
                    price_old = price_tag.select_one('.price-old')
                    if price_old:
                        product_data['original_price'] = price_old.get_text(strip=True)
                else:
                    # Clean up tax lines if present
                    product_data['price'] = price_tag.get_text(strip=True).split('\n')[0]

            products.append(product_data)

        return products

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

if __name__ == "__main__":
    term = input("Enter search term: ")
    results = search_mdcomputers(term)
    
    # Outputting in JSON format
    print(json.dumps(results, indent=2, ensure_ascii=False))
