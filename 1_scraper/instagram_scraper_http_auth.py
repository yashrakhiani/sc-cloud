"""
Instagram Job Post Scraper (HTTP with Authentication - FAST + UNLIMITED!)
Downloads images from @archijobs using HTTP requests with login
Can scrape 500+ posts per day safely
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
LOGIN_USER = os.getenv('INSTAGRAM_LOGIN_USER')
LOGIN_PASS = os.getenv('INSTAGRAM_LOGIN_PASS')
MAX_POSTS = int(os.getenv('MAX_POSTS', 200))
OUTPUT_DIR = Path('data/raw_images')
SESSION_FILE = Path('data/instagram_session_auth.json')

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Instagram API endpoints
LOGIN_URL = "https://www.instagram.com/accounts/login/ajax/"
PROFILE_API = "https://www.instagram.com/api/v1/users/web_profile_info/?username={}"
GRAPHQL_QUERY_HASH = "69cba40317214236af40e7efa697781d"  # User posts query hash

# Headers to mimic real browser
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'X-IG-App-ID': '936619743392459',
    'X-Requested-With': 'XMLHttpRequest',
    'Referer': 'https://www.instagram.com/',
    'Origin': 'https://www.instagram.com'
}


def create_session():
    """Create a requests session with proper headers"""
    session = requests.Session()
    session.headers.update(HEADERS)
    
    # Load saved session if available
    if SESSION_FILE.exists():
        try:
            with open(SESSION_FILE, 'r') as f:
                session_data = json.load(f)
                
            # Restore cookies
            for cookie in session_data.get('cookies', []):
                session.cookies.set(cookie['name'], cookie['value'])
            
            # Restore headers
            if 'csrf_token' in session_data:
                session.headers['X-CSRFToken'] = session_data['csrf_token']
            
            logging.info("✅ Loaded saved authenticated session")
            
            # Verify session is still valid
            if verify_session(session):
                return session
            else:
                logging.warning("Saved session expired, need to re-login")
                
        except Exception as e:
            logging.warning(f"Could not load session: {e}")
    
    return session


def verify_session(session):
    """Check if session is still valid"""
    try:
        response = session.get('https://www.instagram.com/accounts/edit/', timeout=10)
        return response.status_code == 200 and 'login' not in response.url
    except:
        return False


def login(session):
    """Login to Instagram and save session"""
    
    if not LOGIN_USER or not LOGIN_PASS:
        logging.error("❌ Instagram login credentials not set in .env!")
        logging.error("   Set INSTAGRAM_LOGIN_USER and INSTAGRAM_LOGIN_PASS")
        return False
    
    logging.info(f"🔐 Logging in as {LOGIN_USER}...")
    
    try:
        # Get initial cookies and CSRF token
        response = session.get('https://www.instagram.com/accounts/login/', timeout=10)
        csrf_token = session.cookies.get('csrftoken')
        
        if not csrf_token:
            logging.error("Failed to get CSRF token")
            return False
        
        time.sleep(random.uniform(2, 4))
        
        # Login payload
        login_data = {
            'username': LOGIN_USER,
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:{LOGIN_PASS}',
            'queryParams': {},
            'optIntoOneTap': 'false'
        }
        
        # Login headers
        login_headers = {
            'X-CSRFToken': csrf_token,
            'X-Instagram-AJAX': '1',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://www.instagram.com/accounts/login/'
        }
        
        session.headers.update(login_headers)
        
        # Perform login
        response = session.post(LOGIN_URL, data=login_data, timeout=15)
        
        if response.status_code == 200:
            result = response.json()
            
            if result.get('authenticated'):
                logging.info("✅ Login successful!")
                
                # Save session
                session_data = {
                    'cookies': [{'name': c.name, 'value': c.value} for c in session.cookies],
                    'csrf_token': session.cookies.get('csrftoken'),
                    'logged_in_at': datetime.now().isoformat()
                }
                
                with open(SESSION_FILE, 'w') as f:
                    json.dump(session_data, f)
                
                time.sleep(random.uniform(3, 5))
                return True
            else:
                logging.error(f"❌ Login failed: {result.get('message', 'Unknown error')}")
                return False
        else:
            logging.error(f"❌ Login request failed: {response.status_code}")
            return False
            
    except Exception as e:
        logging.error(f"❌ Login error: {e}")
        return False


def get_user_posts(session, username, max_posts=200):
    """Get posts from user profile with pagination"""
    
    logging.info(f"📸 Fetching posts from @{username}...")
    
    try:
        # Get user profile
        url = PROFILE_API.format(username)
        response = session.get(url, timeout=10)
        
        if not response.ok:
            logging.error(f"Failed to get profile: {response.status_code}")
            return []
        
        data = response.json()
        user_data = data.get('data', {}).get('user', {})
        
        if not user_data:
            logging.error("No user data found")
            return []
        
        # Extract posts
        posts = []
        edge_media = user_data.get('edge_owner_to_timeline_media', {})
        edges = edge_media.get('edges', [])
        page_info = edge_media.get('page_info', {})
        
        logging.info(f"Found {len(edges)} posts in initial load")
        
        # Process initial posts
        for edge in edges:
            node = edge.get('node', {})
            posts.append(extract_post_data(node))
        
        # Paginate if we need more posts
        end_cursor = page_info.get('end_cursor')
        has_next = page_info.get('has_next_page', False)
        user_id = user_data.get('id')
        
        while has_next and len(posts) < max_posts and end_cursor:
            logging.info(f"Fetching more posts... (current: {len(posts)})")
            
            # GraphQL query for pagination
            variables = {
                'id': user_id,
                'first': 12,
                'after': end_cursor
            }
            
            params = {
                'query_hash': GRAPHQL_QUERY_HASH,
                'variables': json.dumps(variables)
            }
            
            time.sleep(random.uniform(2, 4))  # Rate limiting
            
            response = session.get(GRAPHQL_API, params=params, timeout=10)
            
            if response.ok:
                data = response.json()
                media_data = data.get('data', {}).get('user', {}).get('edge_owner_to_timeline_media', {})
                edges = media_data.get('edges', [])
                page_info = media_data.get('page_info', {})
                
                for edge in edges:
                    node = edge.get('node', {})
                    posts.append(extract_post_data(node))
                
                end_cursor = page_info.get('end_cursor')
                has_next = page_info.get('has_next_page', False)
            else:
                logging.warning(f"Pagination request failed: {response.status_code}")
                break
        
        logging.info(f"✅ Extracted {len(posts)} posts total")
        return posts[:max_posts]
        
    except Exception as e:
        logging.error(f"Error fetching posts: {e}")
        return []


def extract_post_data(node):
    """Extract relevant data from post node"""
    caption_edges = node.get('edge_media_to_caption', {}).get('edges', [])
    caption = caption_edges[0].get('node', {}).get('text', '') if caption_edges else ''
    
    return {
        'url': node.get('display_url'),
        'shortcode': node.get('shortcode'),
        'caption': caption,
        'timestamp': node.get('taken_at_timestamp', 0),
        'likes': node.get('edge_liked_by', {}).get('count', 0)
    }


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
                        'likes': post.get('likes', 0),
                        'downloaded_at': datetime.now().isoformat(),
                        'index': i
                    }
                    
                    metadata_file = filename.with_suffix('.json')
                    with open(metadata_file, 'w', encoding='utf-8') as f:
                        json.dump(metadata, f, indent=2, ensure_ascii=False)
                    
                    downloaded += 1
                    pbar.update(1)
                    
                    # Rate limiting
                    time.sleep(random.uniform(0.5, 1.5))
                else:
                    logging.warning(f"Failed to download post {i}: {response.status_code}")
                    
            except Exception as e:
                logging.error(f"Error downloading post {i}: {e}")
                continue
    
    return downloaded


def scrape_instagram_authenticated():
    """Main scraping function with authentication"""
    
    logging.info(f"🚀 Starting authenticated scrape of @{TARGET_USERNAME}")
    logging.info(f"   Target: {MAX_POSTS} posts")
    
    # Create session
    session = create_session()
    
    # Login if not already authenticated
    if not verify_session(session):
        if not login(session):
            logging.error("❌ Failed to authenticate. Cannot continue.")
            return 0
    
    # Get posts
    posts = get_user_posts(session, TARGET_USERNAME, MAX_POSTS)
    
    if not posts:
        logging.error("No posts found!")
        return 0
    
    # Download images
    downloaded = download_posts(session, posts, MAX_POSTS)
    
    logging.info(f"✅ Successfully downloaded {downloaded} posts")
    return downloaded


if __name__ == '__main__':
    print("=" * 60)
    print("⚡ StructCrew Instagram Scraper (HTTP + Auth)")
    print("=" * 60)
    print(f"Target: @{TARGET_USERNAME}")
    print(f"Max Posts: {MAX_POSTS}")
    print(f"Output: {OUTPUT_DIR}")
    print("Method: HTTP Requests with Authentication")
    print("Rate Limit: ~500-1000 posts/day safely")
    print("=" * 60)
    print()
    
    result = scrape_instagram_authenticated()
    
    print()
    print("=" * 60)
    print(f"✅ Scraping complete! Downloaded {result} posts")
    print("=" * 60)
