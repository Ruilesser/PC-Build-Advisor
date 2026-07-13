from bs4 import BeautifulSoup
from urllib.parse import quote
import requests
import time

HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 '
        '(Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 '
        '(KHTML, like Gecko) '
        'Chrome/126.0 Safari/537.36'
    )
}

SESSION = requests.Session()
SESSION.headers.update(HEADERS)

# Test searching for a sample part number
part_number = 'CMH32GX5M2B6000Z30'
query = quote(part_number)
search_url = f'https://ca.pcpartpicker.com/search/?q={query}'
print(f'Search URL: {search_url}\n')

try:
    response = SESSION.get(search_url, timeout=20)
    print(f'Status Code: {response.status_code}')
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        links = soup.find_all('a', href=True)
        print(f'Total links found: {len(links)}')
        
        product_links = [link['href'] for link in links if '/product/' in link['href']]
        print(f'Product links found: {len(product_links)}')
        
        if product_links:
            print(f'First product link: {product_links[0]}')
        else:
            print('No product links found')
            # Show some sample links to debug
            print('\nSample links:')
            for i, link in enumerate(links[:10]):
                print(f'  {i}: {link["href"]}')
except Exception as e:
    print(f'Error: {e}')
