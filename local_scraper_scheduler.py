"""
Local Multi-PC Scraper Scheduler
- Scrape 500+ posts daily (split into sessions)
- Deduplicate across all PCs
- Auto-sync database to GitHub
- Track progress globally
"""

import os
import schedule
import time
import logging
from datetime import datetime
from pathlib import Path
import json
import subprocess
from dotenv import load_dotenv

# Setup
load_dotenv()
log_dir = Path('logs')
log_dir.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / 'local_scraper.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class LocalScraperScheduler:
    """Manage local scraping with multi-PC deduplication"""
    
    def __init__(self):
        self.pc_name = os.getenv('PC_NAME', f"pc-{subprocess.run(['whoami'], capture_output=True, text=True).stdout.strip()}")
        self.config = {
            'DAILY_TARGET': 500,
            'POSTS_PER_SESSION': 100,  # 5 sessions × 100 = 500
            'SESSIONS_PER_DAY': 5,
            'SESSION_INTERVAL_HOURS': 4,  # Sessions at 0:00, 4:00, 8:00, 12:00, 16:00
            'STATE_FILE': 'data/local_scraper_state.json',
            'DEDUPE_DB': 'data/scraped_urls.json'
        }
        self.state = self.load_state()

    def load_state(self):
        """Load current scraping state"""
        state_file = Path(self.config['STATE_FILE'])
        if state_file.exists():
            with open(state_file, 'r') as f:
                return json.load(f)
        return {
            'pc_name': self.pc_name,
            'today': str(datetime.now().date()),
            'posts_scraped_today': 0,
            'sessions_completed': 0,
            'total_posts': 0,
            'last_sync': None
        }

    def save_state(self):
        """Save scraping state"""
        state_file = Path(self.config['STATE_FILE'])
        state_file.parent.mkdir(parents=True, exist_ok=True)
        with open(state_file, 'w') as f:
            json.dump(self.state, f, indent=2)

    def reset_daily_counter(self):
        """Reset counter at start of new day"""
        today = str(datetime.now().date())
        if self.state.get('today') != today:
            self.state['today'] = today
            self.state['posts_scraped_today'] = 0
            self.state['sessions_completed'] = 0
            logger.info("🔄 NEW DAY - Resetting daily counters")
            self.save_state()

    def load_dedupe_urls(self):
        """Load all URLs already scraped (across all PCs)"""
        dedupe_file = Path(self.config['DEDUPE_DB'])
        if dedupe_file.exists():
            with open(dedupe_file, 'r') as f:
                return set(json.load(f))
        return set()

    def save_dedupe_urls(self, urls):
        """Save deduplicated URLs"""
        dedupe_file = Path(self.config['DEDUPE_DB'])
        dedupe_file.parent.mkdir(parents=True, exist_ok=True)
        with open(dedupe_file, 'w') as f:
            json.dump(list(urls), f, indent=2)

    def run_scraping_session(self):
        """Run a single scraping session (100 posts)"""
        self.reset_daily_counter()
        
        session_num = self.state['sessions_completed'] + 1
        logger.info("=" * 70)
        logger.info(f"📱 SCRAPING SESSION {session_num}/5 - {self.pc_name}")
        logger.info(f"Target: {self.config['POSTS_PER_SESSION']} posts")
        logger.info("=" * 70)
        
        try:
            # Load existing URLs to avoid duplicates
            existing_urls = self.load_dedupe_urls()
            logger.info(f"Total unique posts in database: {len(existing_urls)}")
            
            # Run scraper with deduplication
            env = os.environ.copy()
            env['MAX_POSTS'] = str(self.config['POSTS_PER_SESSION'])
            env['HEADLESS'] = 'true'
            env['SKIP_EXISTING_URLS'] = 'true'
            
            result = subprocess.run(
                ['python', '1_scraper/instagram_scraper_pro.py'],
                env=env,
                capture_output=True,
                text=True,
                timeout=1800  # 30 minutes per session
            )
            
            if result.returncode == 0:
                # Count newly downloaded images
                new_images = self.get_new_images_count()
                self.state['posts_scraped_today'] += new_images
                self.state['total_posts'] += new_images
                self.state['sessions_completed'] = session_num
                
                logger.info(f"✅ Session {session_num} complete")
                logger.info(f"   New images: {new_images}")
                logger.info(f"   Today's total: {self.state['posts_scraped_today']}/{self.config['DAILY_TARGET']}")
                
                # Check if daily target reached
                if self.state['posts_scraped_today'] >= self.config['DAILY_TARGET']:
                    logger.info(f"🎉 DAILY TARGET REACHED: {self.state['posts_scraped_today']} posts!")
                    self.sync_to_github()
                
            else:
                logger.error(f"❌ Session {session_num} failed: {result.stderr[:500]}")
                
        except subprocess.TimeoutExpired:
            logger.error(f"❌ Session {session_num} timeout (30 min exceeded)")
        except Exception as e:
            logger.error(f"❌ Session {session_num} error: {e}")
        
        self.save_state()

    def get_new_images_count(self):
        """Count newly downloaded images"""
        try:
            image_dir = Path('data/raw_images')
            if image_dir.exists():
                return len(list(image_dir.glob('*.jpg'))) + len(list(image_dir.glob('*.png')))
            return 0
        except:
            return 0

    def sync_to_github(self):
        """Push new posts to GitHub"""
        logger.info("🔄 Syncing to GitHub...")
        
        try:
            # Add new images
            subprocess.run(
                ['git', 'add', 'data/raw_images/', 'data/local_scraper_state.json', 'data/scraped_urls.json'],
                capture_output=True,
                timeout=60
            )
            
            # Commit
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            result = subprocess.run(
                [
                    'git', 'commit',
                    '-m',
                    f"Local scrape: {self.state['posts_scraped_today']} posts ({self.pc_name}) - {timestamp}"
                ],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            # Push
            push_result = subprocess.run(
                ['git', 'push', 'origin', 'main'],
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if push_result.returncode == 0:
                self.state['last_sync'] = datetime.now().isoformat()
                logger.info("✅ GitHub sync complete")
            else:
                logger.error(f"⚠️ Push failed: {push_result.stderr[:200]}")
                
        except Exception as e:
            logger.error(f"⚠️ GitHub sync error: {e}")
        
        self.save_state()

    def schedule_sessions(self):
        """Schedule 5 scraping sessions throughout the day"""
        logger.info("=" * 70)
        logger.info(f"🤖 Local Multi-PC Scraper Scheduler - {self.pc_name}")
        logger.info("=" * 70)
        logger.info(f"Mode: Local scraping (residential IP)")
        logger.info(f"Target: {self.config['DAILY_TARGET']} posts/day")
        logger.info(f"Sessions: {self.config['SESSIONS_PER_DAY']} × {self.config['POSTS_PER_SESSION']} posts")
        logger.info(f"Interval: Every {self.config['SESSION_INTERVAL_HOURS']} hours")
        logger.info("=" * 70)
        logger.info("")
        
        # Schedule sessions at: 00:00, 04:00, 08:00, 12:00, 16:00
        hours = [0, 4, 8, 12, 16]
        for hour in hours:
            time_str = f"{hour:02d}:00"
            schedule.every().day.at(time_str).do(self.run_scraping_session)
            logger.info(f"✓ Scheduled session at {time_str} UTC")
        
        logger.info("")
        logger.info("Waiting for first scheduled session...")

    def run(self):
        """Main scheduler loop"""
        self.schedule_sessions()
        
        # Run first session immediately for testing
        logger.info("\n🚀 Running immediate session for testing...")
        self.run_scraping_session()
        
        # Main loop
        logger.info("\n🔄 Entering scheduling loop...")
        while True:
            try:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
            except KeyboardInterrupt:
                logger.info("\n⛔ Scheduler stopped by user")
                break
            except Exception as e:
                logger.error(f"Scheduler error: {e}")
                time.sleep(300)


if __name__ == "__main__":
    scheduler = LocalScraperScheduler()
    scheduler.run()
