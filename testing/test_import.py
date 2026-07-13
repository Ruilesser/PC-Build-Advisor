print("Testing Selenium import...")
try:
    from selenium import webdriver
    print(" Selenium imported successfully")
except Exception as e:
    print(f" Error importing Selenium: {e}")

print("\nTesting WebDriver setup...")
try:
    from selenium.webdriver.chrome.options import Options
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.service import Service
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    
    print(" WebDriver components imported")
    print(" Ready to create driver")
    
except Exception as e:
    print(f" Error: {e}")
