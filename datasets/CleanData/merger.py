# USE THIS CODE FOR ALL THE DATA THATS WITHIN UserBenchmark CSVs. 
# I built a scraper - it works sort of 
# MAKE SURE TO USE A VPN
# This code uses UserBenchmark's built-in pricing data (by adding #Prices to URLs)
# to extract prices and product names for each part.

import argparse
import re
import time
import atexit

import pandas as pd

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

# TO RUN: python "datasets\CleanData\merger.py" "datasets\PCParts\memory.csv" "datasets\UserBenchmarks\RAM_UserBenchmarks.csv" "datasets\Cleaned\memory_merged.csv"
# Other examples:
#   CPU: python "datasets\CleanData\merger.py" "datasets\PCParts\cpu.csv" "datasets\UserBenchmarks\CPU_UserBenchmarks.csv" "datasets\Cleaned\cpu_merged.csv"
#   GPU: python "datasets\CleanData\merger.py" "datasets\PCParts\video-card.csv" "datasets\UserBenchmarks\GPU_UserBenchmarks.csv" "datasets\Cleaned\video-card_merged.csv"
#   HDD: python "datasets\CleanData\merger.py" "datasets\PCParts\internal-hard-drive.csv" "datasets\UserBenchmarks\HDD_UserBenchmarks.csv" "datasets\Cleaned\internal-hard-drive_merged.csv"


# The script works by using Selenium to load the UserBenchmark pricing pages for each part, extract the price and product name, and then save the results to a new CSV file.


# Initialize Selenium WebDriver
driver = None

def get_driver():
    global driver
    if driver is None:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36")
        
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
    return driver

# Cleanup on exit
def cleanup_driver():
    global driver
    if driver is not None:
        try:
            driver.quit()
        except Exception:
            pass

atexit.register(cleanup_driver)

price_cache = {}
failed_parts = [] # keep track of which parts failed to get info

# taken from cleanup.py 
def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Extract prices and product names from UserBenchmark pricing pages."
    )

    # this one isn't used because merging the part names and numbers was too inefficient, but you can add something that might make it work
    parser.add_argument(
        "parts_csv",
        help="CSV containing original part information (not used, but required for compatibility)."
    )

    parser.add_argument(
        "benchmark_csv",
        help="Benchmark CSV downloaded from UserBenchmark (must have URL and Model columns)."
    )

    parser.add_argument(
        "output_csv",
        help="Output CSV."
    )

    parser.add_argument(
        "--benchmark-url-column",
        default="URL",
        help="Column in benchmark CSV containing the UserBenchmark URL."
    )

    parser.add_argument(
        "--benchmark-model-column",
        default="Model",
        help="Column in benchmark CSV containing the product model name."
    )

    parser.add_argument(
        "--benchmark-rank-column",
        default="Rank",
        help="Rank column."
    )

    return parser.parse_args()

# matching part numbers
def normalize_name(name):
    # Converts a component name into a standardized format for matching.
    if pd.isna(name):
        return ""

    name = str(name).upper().strip()

    # Remove spaces
    name = name.replace(" ", "")

    # Remove common separators
    name = name.replace("-", "")
    name = name.replace("_", "")

    return name

# loading CSV files
# Load UserBenchmark CSV files
def load_data(args):
    benchmark = pd.read_csv(args.benchmark_csv)
    return benchmark

# function to get the page of a URL using Selenium, used for scraping data from the web
def get_page(url, retries=3):
    
    # Downloads a webpage with retries using Selenium. Returns: str | None

    for attempt in range(retries):
        try:
            drv = get_driver()
            drv.get(url)
            # Wait for page to load
            time.sleep(2)
            return drv.page_source

        except Exception as e:
            print(f"        Error loading page: {e}")
            pass

        time.sleep(2 ** attempt)

    return None

# Convert timestamp into days
def parse_timestamp_to_days(timestamp_str):
    try:
        timestamp_str = timestamp_str.strip().lower()
        
        # Handle various formats
        if 'min' in timestamp_str:
            minutes = float(timestamp_str.split()[0])
            return minutes / (24 * 60)  # Convert to days
        elif 'hr' in timestamp_str:
            hours = float(timestamp_str.split()[0])
            return hours / 24  # Convert to days
        elif 'day' in timestamp_str:
            days = float(timestamp_str.split()[0])
            return days
        elif 'week' in timestamp_str:
            weeks = float(timestamp_str.split()[0])
            return weeks * 7
        elif 'month' in timestamp_str:
            months = float(timestamp_str.split()[0])
            return months * 30  # Approximate
        elif 'year' in timestamp_str:
            years = float(timestamp_str.split()[0])
            return years * 365
        else:
            return None
    except (ValueError, IndexError):
        return None

# Extract price from UserBenchmark pricing page within last year
def extract_price_from_page(html):
    if html is None or len(html) < 1000:
        return None

    soup = BeautifulSoup(html, "lxml")
    
    # Find the price link tags (class="bglink vtallp" inside price table)
    price_links = soup.find_all("a", class_="bglink vtallp")
    
    for link in price_links:
        price_text = link.get_text(strip=True)
        
        # Extract price from text like "$610" or "$1,200"
        price_match = re.search(r'\$\s*([0-9,\.]+)', price_text)
        if not price_match:
            continue
        
        try:
            price_str = price_match.group(1).replace(",", "").strip()
            price = float(price_str)
            
            # Find the timestamp in the next span
            timestamp_span = link.find_next("span", class_="prccapt")
            if not timestamp_span:
                continue
            
            timestamp_text = timestamp_span.get_text(strip=True)
            # Remove the info icon text - just get the first part (e.g., "29 days")
            timestamp_only = timestamp_text.split()[0:2]  # Get "29 days" part
            timestamp_only = ' '.join(timestamp_only)
            
            # Check if price is recent (within last year = 365 days)
            days_ago = parse_timestamp_to_days(timestamp_only)
            if days_ago is None or days_ago > 365:
                # Skip old prices
                continue
            
            return price
        except ValueError:
            continue
    
    return None

# loads the UserBenchmark #Prices page and extracts pricing info
def get_prices_for_part(url, model_name):
    if url in price_cache:
        return price_cache[url]
    
    if pd.isna(url) or not url:
        return None, None
    
    # Add #Prices fragment to the URL
    prices_url = f"{url}#Prices"
    
    print(f"        Loading: {prices_url}")
    
    html = get_page(prices_url)
    
    if html is None:
        price_cache[url] = (None, None)
        return None, None
    
    price = extract_price_from_page(html)
    
    result = (model_name, price)
    price_cache[url] = result
    
    if price:
        print(f"        Found price: ${price}")
    else:
        print(f"        No price found")
    
    time.sleep(1)
    
    return result



# IMPORTANT!
# Processes each benchmark entry and extracts pricing from UserBenchmark
def match_parts(benchmark, args):
    output_rows = []
    total = len(benchmark)

    print(f"\nChecking {total} benchmark entries...\n")

    for i, row in benchmark.iterrows():
        url = row[args.benchmark_url_column]
        model = row[args.benchmark_model_column]
        
        print(f"[{i+1}/{total}] {model}")
        
        product_name, price = get_prices_for_part(url, model)
        
        if product_name is not None and price is not None:
            output_rows.append({
                "name": product_name,
                "price": price,
                "rank": row[args.benchmark_rank_column],
                "url": url
            })
        else:
            failed_parts.append(model)

    return pd.DataFrame(output_rows)

# Save output DataFrame to CSV and print summary
def save_results(df, output_csv):
    """Save output DataFrame to CSV and print summary"""
    df.to_csv(output_csv, index=False)

    print("\nFinished!")
    print(f"Saved {len(df)} rows")
    print(f"Output written to:\n{output_csv}")

    if failed_parts:
        print(f"\nFailed to retrieve pricing for {len(failed_parts)} parts:")
        for part in failed_parts[:10]:  # Show first 10
            print(f"  - {part}")
        if len(failed_parts) > 10:
            print(f"  ... and {len(failed_parts) - 10} more")

def main():
    args = parse_arguments()
    print("Loading benchmark data...")

    benchmark = load_data(args)
    print("Extracting prices from UserBenchmark...")

    output = match_parts(benchmark, args)
    save_results(output, args.output_csv)

if __name__ == "__main__":
    main()