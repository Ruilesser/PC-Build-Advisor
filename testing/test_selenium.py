import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from urllib.parse import quote

# Setup Chrome with Selenium
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
# Anti-detection measures
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=chrome_options
)

try:
    # Test searching for a part
    part_number = 'CMH32GX5M2B6000Z30'
    query = quote(part_number)
    search_url = f'https://ca.pcpartpicker.com/search/?q={query}'
    
    print(f"Opening: {search_url}")
    driver.get(search_url)
    
    print("Waiting 5 seconds for page to load...")
    time.sleep(5)
    
    # Get the page source
    html = driver.page_source
    print(f"HTML length: {len(html)}")
    print("\nFirst 1000 chars:")
    print(html[:1000])
    
    # Try to parse with BeautifulSoup
    soup = BeautifulSoup(html, 'lxml')
    links = soup.find_all('a', href=True)
    print(f"\nTotal links found: {len(links)}")
    
    product_links = [link['href'] for link in links if '/product/' in link['href']]
    print(f"Product links found: {len(product_links)}")
    
    if product_links:
        print(f"First product link: {product_links[0]}")
    
finally:
    driver.quit()
