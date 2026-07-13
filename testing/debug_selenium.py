print("Starting test...")

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from urllib.parse import quote
import time

print("Imports successful")

# Setup Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
# Anti-detection measures
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

print("Creating WebDriver...")
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=chrome_options
)

print("WebDriver created. Loading PCPartPicker...")
try:
    driver.get('https://ca.pcpartpicker.com/search/?q=CMH32GX5M2B6000Z30')
    print("Page loaded. Waiting 5 seconds...")
    time.sleep(5)
    
    html = driver.page_source
    print(f"\nHTML size: {len(html)} characters")
    print("\nFirst 500 chars:")
    print(html[:500])
    
    if "unavailable" in html.lower():
        print("\n⚠ PCPartPicker is unavailable - likely blocked")
    elif "search" in html.lower():
        print("\n Page contains search content")
    else:
        print("\n? Unable to determine page status")
        
except Exception as e:
    print(f"Error: {e}")
    
finally:
    driver.quit()
    print("\nWebDriver closed")
