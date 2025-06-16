import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://commons.wikimedia.org"
CATEGORY_URL = f"{BASE_URL}/wiki/Category:PNG_chess_pieces/Standard_transparent"
OUTPUT_DIR = "chess_pieces"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Step 1: Load category page
resp = requests.get(CATEGORY_URL)
soup = BeautifulSoup(resp.content, "html.parser")

# Step 2: Find all links to individual file pages
gallery_links = soup.select('div.gallerytext a')
file_page_urls = [urljoin(BASE_URL, a["href"]) for a in gallery_links]

# Step 3: Download PNGs from each file page
for file_url in file_page_urls:
    file_resp = requests.get(file_url)
    file_soup = BeautifulSoup(file_resp.content, "html.parser")
    img_tag = file_soup.select_one("div.fullMedia a")
    
    if img_tag and img_tag["href"].endswith(".png"):
        img_url = urljoin(BASE_URL, img_tag["href"])
        img_data = requests.get(img_url).content
        filename = os.path.join(OUTPUT_DIR, os.path.basename(img_url))
        
        with open(filename, "wb") as f:
            f.write(img_data)
        print(f"Downloaded: {filename}")