import requests
from urllib.parse import quote

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'
}

SESSION = requests.Session()
SESSION.headers.update(HEADERS)

part_number = 'CMH32GX5M2B6000Z30'
query = quote(part_number)
search_url = f'https://ca.pcpartpicker.com/search/?q={query}'

response = SESSION.get(search_url, timeout=20)
html = response.text

# Check first 2000 characters
print("First 2000 chars of HTML:")
print(html[:2000])
print('\n...\n')

# Check if it contains keywords
if 'search' in html.lower():
    print('Found "search" in HTML')
if 'javascript' in html.lower():
    print(' Page uses JavaScript - likely dynamic loading')
if '<div' in html.lower():
    print(' Found div elements')
else:
    print(' No div elements found - page structure is minimal')

print(f'\nTotal HTML length: {len(html)} characters')
