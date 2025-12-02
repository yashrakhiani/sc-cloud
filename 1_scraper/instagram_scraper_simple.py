"""
Instagram Scraper - Simple Public Profile Version
No login needed - scrapes public posts directly
"""

import os
import json
import time
import random
import requests
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
import logging
from tqdm import tqdm

# Setup
load_dotenv()
if Path('.env.production').exists():
    load_dotenv('.env.production')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/scraper.log'),
        logging.StreamHandler()
    ]
)

# Configuration
TARGET_USERNAME = os.getenv('INSTAGRAM_USERNAME', 'archijobs')
MAX_POSTS = int(os.getenv('MAX_POSTS', 500))
OUTPUT_DIR = Path('data/raw_images')

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def scrape_instagram_simple():
    """Scrape Instagram public profile - no login needed"""
    
    logging.info(f"🚀 Scraping @{TARGET_USERNAME} (public profile)")
    logging.info(f"   Target: {MAX_POSTS} posts")
    
    # Instagram public profile URL
    url = f"https://www.instagram.com/{TARGET_USERNAME}/?__a=1&__d=dis"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    
    session = requests.Session()
    session.headers.update(headers)
    
    try:
        # Get the profile page HTML
        response = session.get(f"https://www.instagram.com/{TARGET_USERNAME}/", timeout=10)
        
        if response.status_code != 200:
            logging.error(f"Failed to access profile: {response.status_code}")
            return 0
        
        # Extract JSON data from HTML
        html = response.text
        
        # Find the shared data JSON
        start_marker = 'window._sharedData = '
        end_marker = ';</script>'
        
        start_idx = html.find(start_marker)
        if start_idx == -1:
            logging.error("Could not find shared data in HTML")
            # Try alternative method - scrape image URLs directly from HTML
            return scrape_from_html(html, session)
        
        start_idx += len(start_marker)
        end_idx = html.find(end_marker, start_idx)
        
        if end_idx == -1:
            logging.error("Could not parse shared data")
            return scrape_from_html(html, session)
        
        json_str = html[start_idx:end_idx]
        data = json.loads(json_str)
        
        # Navigate to posts
        user_data = data['entry_data']['ProfilePage'][0]['graphql']['user']
        edges = user_data['edge_owner_to_timeline_media']['edges']
        
        logging.info(f"Found {len(edges)} posts")
        
        # Download posts
        downloaded = 0
        for i, edge in enumerate(edges[:MAX_POSTS]):
            node = edge['node']
            image_url = node['display_url']
            
            try:
                img_response = session.get(image_url, timeout=15)
                if img_response.status_code == 200:
                    filename = OUTPUT_DIR / f'post_{i:05d}.jpg'
                    with open(filename, 'wb') as f:
                        f.write(img_response.content)
                    
                    # Save metadata
                    metadata = {
                        'filename': filename.name,
                        'url': image_url,
                        'shortcode': node.get('shortcode', ''),
                        'caption': node.get('edge_media_to_caption', {}).get('edges', [{}])[0].get('node', {}).get('text', ''),
                        'downloaded_at': datetime.now().isoformat(),
                        'index': i
                    }
                    
                    metadata_file = filename.with_suffix('.json')
                    with open(metadata_file, 'w', encoding='utf-8') as f:
                        json.dump(metadata, f, indent=2, ensure_ascii=False)
                    
                    downloaded += 1
                    logging.info(f"✅ Downloaded: post_{i:05d}.jpg")
                    
                    time.sleep(random.uniform(0.5, 1.5))
                    
            except Exception as e:
                logging.error(f"Error downloading post {i}: {e}")
                continue
        
        logging.info(f"✅ Successfully downloaded {downloaded} posts")
        return downloaded
        
    except Exception as e:
        logging.error(f"Error scraping Instagram: {e}")
        return 0

def scrape_from_html(html, session):
    """Fallback: Extract image URLs directly from HTML"""
    logging.info("Using fallback HTML scraping method...")
    
    import re
    
    # Find all image URLs in HTML
    pattern = r'https://[^"]+\.cdninstagram\.com/[^"]+\.jpg[^"]*'
    image_urls = re.findall(pattern, html)
    
    # Remove duplicates and filter
    image_urls = list(set(image_urls))
    image_urls = [url for url in image_urls if 's640x640' in url or 's1080x1080' in url]
    
    logging.info(f"Found {len(image_urls)} image URLs in HTML")
    
    downloaded = 0
    for i, url in enumerate(image_urls[:MAX_POSTS]):
        try:
            response = session.get(url, timeout=15)
            if response.status_code == 200:
                filename = OUTPUT_DIR / f'post_{i:05d}.jpg'
                with open(filename, 'wb') as f:
                    f.write(response.content)
                
                downloaded += 1
                logging.info(f"✅ Downloaded: post_{i:05d}.jpg")
                time.sleep(random.uniform(0.5, 1.5))
                
        except Exception as e:
            logging.error(f"Error downloading image {i}: {e}")
            continue
    
    logging.info(f"✅ Downloaded {downloaded} posts via HTML scraping")
    return downloaded

if __name__ == '__main__':
    print("=" * 60)
    print("StructCrew Instagram Scraper (Simple)")
    print("=" * 60)
    print(f"Target: @{TARGET_USERNAME}")
    print(f"Max Posts: {MAX_POSTS}")
    print(f"Output: {OUTPUT_DIR}")
    print("Method: Public profile (no login)")
    print("=" * 60)
    print()
    
    result = scrape_instagram_simple()
    
    print()
    print("=" * 60)
    print(f"Scraping complete! Downloaded {result} posts")
    print("=" * 60)
