"""
Instagram Job Post Scraper (HTTP-based - FAST!)
Downloads images from @archijobs using HTTP requests only
Author: StructCrew Lead Generation System
Updated: Dec 1, 2025
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
MAX_POSTS = int(os.getenv('MAX_POSTS', 200))
OUTPUT_DIR = Path('data/raw_images')
SESSION_FILE = Path('data/instagram_session.json')

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Instagram API endpoints (unofficial but works)
PROFILE_API = "https://www.instagram.com/api/v1/users/web_profile_info/?username={}"
GRAPHQL_API = "https://www.instagram.com/graphql/query/"

# Headers to mimic real browser
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'X-IG-App-ID': '936619743392459',  # Instagram web app ID
    'X-Requested-With': 'XMLHttpRequest',
    'Referer': 'https://www.instagram.com/',
    'Origin': 'https://www.instagram.com'
}


def create_session():
    """Create a requests session with proper headers"""
    session = requests.Session()
    session.headers.update(HEADERS)
    
    # Load saved cookies if available
    if SESSION_FILE.exists():
        try:
            with open(SESSION_FILE, 'r') as f:
                cookies = json.load(f)
                for cookie in cookies:
                    session.cookies.set(cookie['name'], cookie['value'])
            logging.info("Loaded saved session cookies")
        except Exception as e:
            logging.warning(f"Could not load session: {e}")
    
    # Get initial cookies by visiting Instagram homepage
    try:
        response = session.get('https://www.instagram.com/', timeout=10)
        if response.ok:
            logging.info("Session initialized successfully")
            save_session(session)
        else:
            logging.warning(f"Session init returned status {response.status_code}")
    except Exception as e:
        logging.error(f"Failed to initialize session: {e}")
    
    return session


def save_session(session):
    """Save session cookies for reuse"""
    cookies = [{'name': c.name, 'value': c.value} for c in session.cookies]
    with open(SESSION_FILE, 'w') as f:
        json.dump(cookies, f)


def get_user_id(session, username):
    """Get Instagram user ID from username"""
    try:
        url = PROFILE_API.format(username)
        response = session.get(url, timeout=10)
        
        if response.ok:
            data = response.json()
            user_data = data.get('data', {}).get('user', {})
            user_id = user_data.get('id')
            
            if user_id:
                logging.info(f"Found user ID for @{username}: {user_id}")
                return user_id, user_data
        else:
            logging.error(f"Failed to get user profile: {response.status_code}")
            
    except Exception as e:
        logging.error(f"Error getting user ID: {e}")
    
    return None, None


def get_posts_from_profile(session, username, max_posts=200):
    """Get posts from a public Instagram profile"""
    
    logging.info(f"Fetching posts from @{username}...")
    
    # Get user ID first
    user_id, user_data = get_user_id(session, username)
    
    if not user_id:
        logging.error("Could not get user ID. Profile might be private or username is wrong.")
        return []
    
    # Get posts from edge_owner_to_timeline_media
    posts = []
    edge_media = user_data.get('edge_owner_to_timeline_media', {})
    edges = edge_media.get('edges', [])
    
    logging.info(f"Found {len(edges)} posts in initial load")
    
    for edge in edges[:max_posts]:
        node = edge.get('node', {})
        
        # Get the display URL (main image)
        display_url = node.get('display_url')
        shortcode = node.get('shortcode')
        caption_edges = node.get('edge_media_to_caption', {}).get('edges', [])
        caption = caption_edges[0].get('node', {}).get('text', '') if caption_edges else ''
        
        if display_url:
            posts.append({
                'url': display_url,
                'shortcode': shortcode,
                'caption': caption,
                'timestamp': node.get('taken_at_timestamp', 0)
            })
    
    # If we need more posts, we'd need to paginate (requires end_cursor)
    # For now, Instagram typically loads 12 posts initially
    
    logging.info(f"Extracted {len(posts)} posts")
    return posts


def download_posts(session, posts, max_downloads=200):
    """Download post images"""
    
    downloaded = 0
    
    with tqdm(total=min(len(posts), max_downloads), desc="Downloading posts") as pbar:
        for i, post in enumerate(posts[:max_downloads]):
            try:
                # Download image
                response = session.get(post['url'], timeout=15)
                
                if response.ok:
                    filename = OUTPUT_DIR / f'post_{i:05d}.jpg'
                    with open(filename, 'wb') as f:
                        f.write(response.content)
                    
                    # Save metadata
                    metadata = {
                        'filename': filename.name,
                        'url': post['url'],
                        'shortcode': post['shortcode'],
                        'caption': post['caption'],
                        'downloaded_at': datetime.now().isoformat(),
                        'index': i
                    }
                    
                    metadata_file = filename.with_suffix('.json')
                    with open(metadata_file, 'w', encoding='utf-8') as f:
                        json.dump(metadata, f, indent=2, ensure_ascii=False)
                    
                    downloaded += 1
                    pbar.update(1)
                    
                    # Small delay to be respectful
                    time.sleep(random.uniform(0.5, 1.5))
                else:
                    logging.warning(f"Failed to download post {i}: {response.status_code}")
                    
            except Exception as e:
                logging.error(f"Error downloading post {i}: {e}")
                continue
    
    return downloaded


def scrape_instagram_fast():
    """Main scraping function - HTTP only, no browser!"""
    
    logging.info(f"Starting FAST scrape of @{TARGET_USERNAME} - Target: {MAX_POSTS} posts")
    
    # Create session
    session = create_session()
    
    # Get posts
    posts = get_posts_from_profile(session, TARGET_USERNAME, MAX_POSTS)
    
    if not posts:
        logging.error("No posts found! Profile might be private or rate limited.")
        return 0
    
    # Download images
    downloaded = download_posts(session, posts, MAX_POSTS)
    
    logging.info(f"✅ Successfully downloaded {downloaded} posts")
    return downloaded


if __name__ == '__main__':
    print("=" * 60)
    print("⚡ StructCrew Instagram Scraper (FAST MODE)")
    print("=" * 60)
    print(f"Target: @{TARGET_USERNAME}")
    print(f"Max Posts: {MAX_POSTS}")
    print(f"Output: {OUTPUT_DIR}")
    print("Method: HTTP Requests (No Browser!)")
    print("=" * 60)
    print()
    
    result = scrape_instagram_fast()
    
    print()
    print("=" * 60)
    print(f"✅ Scraping complete! Downloaded {result} posts")
    print("=" * 60)
