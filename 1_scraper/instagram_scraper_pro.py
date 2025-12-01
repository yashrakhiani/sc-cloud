"""
Instagram Job Post Scraper (Playwright-based)
Downloads images from @archijobs with anti-ban protections
Author: StructCrew Lead Generation System
Updated: Nov 27, 2025
"""

import os
import json
import time
import random
from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
from tqdm import tqdm
from dotenv import load_dotenv
import logging

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
MAX_POSTS = int(os.getenv('MAX_POSTS', 500))  # Start with 500
OUTPUT_DIR = Path('data/raw_images')
COOKIES_FILE = Path('data/instagram_cookies.json')
HEADLESS = os.getenv('HEADLESS', 'false').lower() == 'true'

# Anti-ban settings
SCROLL_DELAY = (3, 7)  # Random delay between scrolls (seconds)
DOWNLOAD_DELAY = (2, 4)  # Random delay between downloads
MAX_RETRIES = 3

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def human_delay(min_sec=1, max_sec=3):
    """Random human-like delay"""
    time.sleep(random.uniform(min_sec, max_sec))


def save_cookies(context, filepath):
    """Save browser cookies for session persistence"""
    cookies = context.cookies()
    with open(filepath, 'w') as f:
        json.dump(cookies, f)
    logging.info(f"Cookies saved to {filepath}")


def load_cookies(context, filepath):
    """Load saved cookies"""
    if filepath.exists():
        with open(filepath, 'r') as f:
            cookies = json.load(f)
        context.add_cookies(cookies)
        logging.info(f"Cookies loaded from {filepath}")
        return True
    return False


def scrape_instagram_posts():
    """Main scraping function"""
    logging.info(f"Starting scrape of @{TARGET_USERNAME} - Target: {MAX_POSTS} posts")
    
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(
            headless=HEADLESS,
            args=['--disable-blink-features=AutomationControlled']  # Anti-detection
        )
        
        # Create context with realistic fingerprint
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        
        page = context.new_page()
        
        # Load cookies if available, otherwise manual login needed
        cookies_loaded = load_cookies(context, COOKIES_FILE)
        
        try:
            # Navigate to profile
            logging.info(f"Navigating to https://instagram.com/{TARGET_USERNAME}")
            page.goto(f'https://instagram.com/{TARGET_USERNAME}', wait_until='networkidle')
            human_delay(3, 5)
            
            # Check if login is needed
            if not cookies_loaded or 'login' in page.url:
                logging.info("🍪 Cookies not found or expired. Logging in...")
                
                login_user = os.getenv('INSTAGRAM_LOGIN_USER')
                login_pass = os.getenv('INSTAGRAM_LOGIN_PASS')
                
                if login_user and login_pass:
                    try:
                        logging.info(f"Attempting auto-login as {login_user}...")
                        page.goto('https://www.instagram.com/accounts/login/', wait_until='networkidle')
                        human_delay(2, 4)
                        
                        # Accept cookies if prompted
                        try:
                            page.click('button:has-text("Allow all cookies")', timeout=3000)
                        except:
                            pass
                            
                        # Fill login form
                        page.fill('input[name="username"]', login_user)
                        human_delay(1, 2)
                        page.fill('input[name="password"]', login_pass)
                        human_delay(1, 2)
                        
                        # Click login
                        page.click('button[type="submit"]')
                        logging.info("Clicked login button. Waiting for navigation...")
                        page.wait_for_navigation(timeout=15000)
                        human_delay(3, 5)
                        
                        # Save cookies
                        save_cookies(context, COOKIES_FILE)
                        logging.info("✅ Auto-login successful! Cookies saved.")
                        
                    except Exception as e:
                        logging.error(f"Auto-login failed: {e}")
                        logging.warning("⚠️ Please log in manually in the browser window...")
                        time.sleep(60)
                else:
                    logging.warning("⚠️ No login credentials found in .env!")
                    logging.warning("Please log in manually in the browser window...")
                    logging.warning("Waiting 60 seconds for manual login...")
                    time.sleep(60)
                    save_cookies(context, COOKIES_FILE)
            
            # Wait for posts to load
            page.wait_for_selector('article img', timeout=10000)
            
            posts_collected = 0
            downloaded_urls = set()
            last_height = 0
            no_new_posts_count = 0
            
            with tqdm(total=MAX_POSTS, desc="Downloading posts") as pbar:
                while posts_collected < MAX_POSTS:
                    # Find all post images on current viewport
                    posts = page.query_selector_all('article img[src^="https://"]')
                    
                    for img in posts:
                        if posts_collected >= MAX_POSTS:
                            break
                        
                        # Get image source
                        src = img.get_attribute('src')
                        if not src or src in downloaded_urls:
                            continue
                        
                        # Get alt text for job filtering
                        alt_text = img.get_attribute('alt') or ''
                        
                        # Filter for job-related posts (optional)
                        # Uncomment to only download job posts:
                        # job_keywords = ['job', 'hiring', 'architect', 'position', 'opening']
                        # if not any(keyword in alt_text.lower() for keyword in job_keywords):
                        #     continue
                        
                        try:
                            # Download image
                            response = page.request.get(src)
                            if response.ok:
                                filename = OUTPUT_DIR / f'post_{posts_collected:05d}.jpg'
                                with open(filename, 'wb') as f:
                                    f.write(response.body())
                                
                                # Save metadata
                                metadata = {
                                    'filename': filename.name,
                                    'url': src,
                                    'alt_text': alt_text,
                                    'downloaded_at': datetime.now().isoformat(),
                                    'index': posts_collected
                                }
                                
                                metadata_file = filename.with_suffix('.json')
                                with open(metadata_file, 'w') as f:
                                    json.dump(metadata, f, indent=2)
                                
                                downloaded_urls.add(src)
                                posts_collected += 1
                                pbar.update(1)
                                
                                logging.debug(f"Downloaded: {filename.name}")
                                human_delay(*DOWNLOAD_DELAY)
                        
                        except Exception as e:
                            logging.error(f"Error downloading image: {e}")
                            continue
                    
                    # Scroll to load more posts
                    current_height = page.evaluate('document.body.scrollHeight')
                    
                    if current_height == last_height:
                        no_new_posts_count += 1
                        if no_new_posts_count >= 3:
                            logging.warning("No new posts loaded after 3 attempts. Stopping.")
                            break
                    else:
                        no_new_posts_count = 0
                    
                    last_height = current_height
                    
                    # Scroll down
                    page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
                    human_delay(*SCROLL_DELAY)
            
            logging.info(f"✅ Successfully downloaded {posts_collected} posts")
            
        except PlaywrightTimeout:
            logging.error("Timeout while loading Instagram. Check your internet connection.")
        
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
        
        finally:
            # Save cookies for next run
            save_cookies(context, COOKIES_FILE)
            browser.close()
    
    return posts_collected


if __name__ == '__main__':
    print("=" * 60)
    print("📸 StructCrew Instagram Scraper")
    print("=" * 60)
    print(f"Target: @{TARGET_USERNAME}")
    print(f"Max Posts: {MAX_POSTS}")
    print(f"Output: {OUTPUT_DIR}")
    print(f"Headless: {HEADLESS}")
    print("=" * 60)
    print()
    
    result = scrape_instagram_posts()
    
    print()
    print("=" * 60)
    print(f"✅ Scraping complete! Downloaded {result} posts")
    print("=" * 60)
