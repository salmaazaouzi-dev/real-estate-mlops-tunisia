import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

BASE_URL = "https://www.mubawab.tn/fr/sc/appartements-a-vendre"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7"
}

def scrape_listings(max_pages=2):
    listings_data = []

    for page in range(1, max_pages + 1):
        url = f"{BASE_URL}:p:{page}"
        print(f"[INFO] Fetching page {page}: {url}")
        
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            print(f"[ERROR] Failed to retrieve page {page} - Status Code: {response.status_code}")
            continue

        soup = BeautifulSoup(response.content, "html.parser")
        
        # Target all listing containers flexibility
        ads = soup.find_all(["li", "div"], class_=lambda x: x and "listingBox" in x)
        
        if not ads:
            # Fallback selector if listingBox class is dynamic
            ads = soup.select(".listingBox, [class*='listing-']")

        for ad in ads:
            try:
                title_elem = ad.find(["h2", "h3"]) or ad.select_one("[class*='title']")
                price_elem = ad.select_one(".priceTag, [class*='price']")
                loc_elem = ad.select_one(".listingDetails, [class*='location']")
                
                title = title_elem.text.strip() if title_elem else "N/A"
                price = price_elem.text.strip() if price_elem else "N/A"
                location = loc_elem.text.strip() if loc_elem else "N/A"
                
                details = [span.text.strip() for span in ad.find_all("span") if span.text.strip()]
                
                if title != "N/A" or price != "N/A":
                    listings_data.append({
                        "title": title,
                        "price": price,
                        "location": location,
                        "details": " | ".join(details[:5])
                    })
            except Exception as e:
                print(f"[WARNING] Error parsing ad: {e}")

        time.sleep(2)

    output_dir = "data/raw"
    os.makedirs(output_dir, exist_ok=True)
    df = pd.DataFrame(listings_data)
    df.to_csv(f"{output_dir}/raw_real_estate.csv", index=False)
    print(f"[SUCCESS] Scraped {len(df)} listings and saved to {output_dir}/raw_real_estate.csv")

if __name__ == "__main__":
    scrape_listings(max_pages=10)