"""
Complete Daily Automation Manager
Manages: 500 unique posts scraped + 500 emails sent per day
Runs in cloud with persistent database
Author: StructCrew Lead Generation
"""

import time
import subprocess
import os
import schedule
import logging
from datetime import datetime, timedelta
from pathlib import Path
import json
import sqlite3

# Setup logging
log_dir = Path('logs')
log_dir.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / 'automation_manager.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class AutomationManager:
    def __init__(self):
        self.config = {
            'DAILY_POSTS_TARGET': 500,      # Posts to scrape per day
            'DAILY_EMAIL_TARGET': 500,      # Emails to send per day
            'SCRAPE_START_HOUR': 2,         # Start scraping at 2 AM UTC (off-peak)
            'OCR_START_HOUR': 4,            # OCR at 4 AM UTC
            'EMAIL_START_HOUR': 9,          # Send emails at 9 AM UTC
            'STATE_FILE': 'data/automation_state.json'
        }
        self.state = self.load_state()

    def load_state(self):
        """Load automation state from file"""
        state_file = Path(self.config['STATE_FILE'])
        if state_file.exists():
            with open(state_file, 'r') as f:
                return json.load(f)
        return {
            'last_scrape_date': None,
            'posts_scraped_today': 0,
            'emails_sent_today': 0,
            'last_successful_run': None,
            'current_phase': 'idle'
        }

    def save_state(self):
        """Save automation state to file"""
        state_file = Path(self.config['STATE_FILE'])
        state_file.parent.mkdir(parents=True, exist_ok=True)
        with open(state_file, 'w') as f:
            json.dump(self.state, f, indent=2)

    def is_new_day(self):
        """Check if it's a new day (UTC)"""
        last_scrape = self.state['last_scrape_date']
        if not last_scrape:
            return True
        
        last_date = datetime.fromisoformat(last_scrape).date()
        today = datetime.utcnow().date()
        return last_date < today

    def reset_daily_counters(self):
        """Reset counters at start of new day"""
        if self.is_new_day():
            logger.info("🔄 NEW DAY - Resetting counters")
            self.state['posts_scraped_today'] = 0
            self.state['emails_sent_today'] = 0
            self.state['last_scrape_date'] = datetime.utcnow().isoformat()
            self.save_state()

    def run_scraper(self):
        """Phase 1: Scrape Instagram posts"""
        self.reset_daily_counters()
        
        logger.info("=" * 70)
        logger.info("🌍 PHASE 1: INSTAGRAM SCRAPER (500 posts)")
        logger.info("=" * 70)
        
        self.state['current_phase'] = 'scraping'
        self.save_state()
        
        try:
            # Get current posts count from database
            posts_in_db = self.get_posts_count()
            posts_needed = self.config['DAILY_POSTS_TARGET'] - self.state['posts_scraped_today']
            
            logger.info(f"Posts in DB: {posts_in_db}")
            logger.info(f"Posts needed today: {posts_needed}")
            
            # Run scraper
            env = os.environ.copy()
            env['MAX_POSTS'] = str(posts_needed)
            env['HEADLESS'] = 'true'
            
            result = subprocess.run(
                ['python', '1_scraper/instagram_scraper_pro.py'],
                env=env,
                capture_output=True,
                text=True,
                timeout=7200  # 2 hours max
            )
            
            if result.returncode == 0:
                # Count newly downloaded images
                new_count = self.get_new_images_count()
                self.state['posts_scraped_today'] = new_count
                logger.info(f"✅ Scraping complete. New images: {new_count}")
            else:
                logger.error(f"❌ Scraper failed: {result.stderr}")
                self.state['posts_scraped_today'] = 0
                
        except subprocess.TimeoutExpired:
            logger.error("❌ Scraper timeout (2 hours exceeded)")
        except Exception as e:
            logger.error(f"❌ Scraper error: {e}")
        
        self.save_state()

    def run_ocr(self):
        """Phase 2: Extract text from images via OCR"""
        logger.info("=" * 70)
        logger.info("🔍 PHASE 2: OCR TEXT EXTRACTION")
        logger.info("=" * 70)
        
        self.state['current_phase'] = 'ocr'
        self.save_state()
        
        try:
            result = subprocess.run(
                ['python', '2_ocr/process_images_pro.py'],
                capture_output=True,
                text=True,
                timeout=3600  # 1 hour max
            )
            
            if result.returncode == 0:
                logger.info("✅ OCR extraction complete")
            else:
                logger.error(f"⚠️ OCR had issues: {result.stderr[:500]}")
                
        except subprocess.TimeoutExpired:
            logger.error("❌ OCR timeout (1 hour exceeded)")
        except Exception as e:
            logger.error(f"❌ OCR error: {e}")

    def run_email_extraction(self):
        """Phase 3: Extract emails and build database"""
        logger.info("=" * 70)
        logger.info("⛏️ PHASE 3: EMAIL EXTRACTION & DATABASE")
        logger.info("=" * 70)
        
        self.state['current_phase'] = 'extraction'
        self.save_state()
        
        try:
            result = subprocess.run(
                ['python', '3_email_extractor/extract_emails_pro.py'],
                capture_output=True,
                text=True,
                timeout=1800  # 30 minutes
            )
            
            if result.returncode == 0:
                logger.info("✅ Email extraction complete")
            else:
                logger.error(f"⚠️ Extraction had issues: {result.stderr[:500]}")
                
        except subprocess.TimeoutExpired:
            logger.error("❌ Extraction timeout")
        except Exception as e:
            logger.error(f"❌ Extraction error: {e}")

    def run_email_campaign(self):
        """Phase 4: Send 500 emails"""
        logger.info("=" * 70)
        logger.info("📧 PHASE 4: EMAIL CAMPAIGN (500 emails)")
        logger.info("=" * 70)
        
        self.state['current_phase'] = 'sending'
        self.save_state()
        
        try:
            # Set daily limit to 500
            env = os.environ.copy()
            env['DAILY_EMAIL_LIMIT'] = '500'
            
            result = subprocess.run(
                ['python', '4_email_sender/send_campaign_pro.py', '--live', '--auto'],
                env=env,
                capture_output=True,
                text=True,
                timeout=3600  # 1 hour
            )
            
            if result.returncode == 0:
                # Count sent emails
                sent_count = self.get_sent_emails_count()
                self.state['emails_sent_today'] = sent_count
                logger.info(f"✅ Email campaign complete. Emails sent: {sent_count}")
            else:
                logger.error(f"⚠️ Email sending had issues: {result.stderr[:500]}")
                
        except subprocess.TimeoutExpired:
            logger.error("❌ Email sending timeout")
        except Exception as e:
            logger.error(f"❌ Email sending error: {e}")

    def run_full_pipeline(self):
        """Run complete daily pipeline"""
        logger.info("\n" + "=" * 70)
        logger.info("🚀 STARTING DAILY AUTOMATION PIPELINE")
        logger.info(f"Time: {datetime.utcnow().isoformat()}")
        logger.info("=" * 70 + "\n")
        
        start_time = time.time()
        
        try:
            # Phase 1: Scrape (ONLY during off-peak, can skip if just sending)
            if self.should_scrape_today():
                self.run_scraper()
            else:
                logger.info("⏭️ Skipping scraper (enough posts for today)")
            
            # Phase 2: OCR
            self.run_ocr()
            
            # Phase 3: Email Extraction
            self.run_email_extraction()
            
            # Phase 4: Send Emails
            self.run_email_campaign()
            
            # Summary
            elapsed = time.time() - start_time
            logger.info("\n" + "=" * 70)
            logger.info("✅ DAILY PIPELINE COMPLETE")
            logger.info(f"Duration: {elapsed/60:.1f} minutes")
            logger.info(f"Posts scraped: {self.state['posts_scraped_today']}")
            logger.info(f"Emails sent: {self.state['emails_sent_today']}")
            logger.info("=" * 70 + "\n")
            
            self.state['current_phase'] = 'idle'
            self.state['last_successful_run'] = datetime.utcnow().isoformat()
            self.save_state()
            
        except Exception as e:
            logger.error(f"❌ PIPELINE FAILED: {e}")
            self.state['current_phase'] = 'error'
            self.save_state()

    def should_scrape_today(self):
        """Check if we need to scrape more posts"""
        try:
            conn = sqlite3.connect('data/leads.db')
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM raw_posts WHERE date(created_at) = date('now')")
            today_count = cursor.fetchone()[0]
            conn.close()
            
            return today_count < self.config['DAILY_POSTS_TARGET']
        except:
            return True  # Default to scraping if DB error

    def get_posts_count(self):
        """Get total posts in database"""
        try:
            conn = sqlite3.connect('data/leads.db')
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM raw_posts")
            count = cursor.fetchone()[0]
            conn.close()
            return count
        except:
            return 0

    def get_new_images_count(self):
        """Get count of newly downloaded images"""
        try:
            image_dir = Path('data/raw_images')
            if image_dir.exists():
                return len(list(image_dir.glob('*.jpg'))) + len(list(image_dir.glob('*.png')))
            return 0
        except:
            return 0

    def get_sent_emails_count(self):
        """Get count of emails sent today"""
        try:
            conn = sqlite3.connect('data/leads.db')
            cursor = conn.cursor()
            cursor.execute(
                "SELECT COUNT(*) FROM emails WHERE status = 'sent' AND date(sent_at) = date('now')"
            )
            count = cursor.fetchone()[0]
            conn.close()
            return count
        except:
            return 0

    def schedule_jobs(self):
        """Schedule all daily jobs"""
        logger.info("📅 Scheduling daily automation tasks...")
        
        # Run at specific UTC times
        schedule.every().day.at("02:00").do(self.run_scraper)      # 2 AM UTC
        schedule.every().day.at("04:00").do(self.run_ocr)          # 4 AM UTC
        schedule.every().day.at("05:00").do(self.run_email_extraction)  # 5 AM UTC
        schedule.every().day.at("09:00").do(self.run_full_pipeline) # 9 AM UTC (full run)
        
        logger.info("✅ Scheduled:")
        logger.info("  • 02:00 UTC: Instagram scraper (500 posts)")
        logger.info("  • 04:00 UTC: OCR text extraction")
        logger.info("  • 05:00 UTC: Email extraction")
        logger.info("  • 09:00 UTC: Full pipeline + email campaign (500 emails)")

    def run(self):
        """Main automation loop"""
        logger.info("=" * 70)
        logger.info("🤖 StructCrew Automation Manager v2.0")
        logger.info("=" * 70)
        logger.info(f"Daily Targets: {self.config['DAILY_POSTS_TARGET']} posts + {self.config['DAILY_EMAIL_TARGET']} emails")
        logger.info("Mode: Cloud Automation (Off-peak scraping)")
        logger.info("=" * 70 + "\n")
        
        self.schedule_jobs()
        
        # Run first pipeline immediately
        self.run_full_pipeline()
        
        # Main loop
        logger.info("🔄 Entering main scheduling loop...")
        while True:
            try:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
            except KeyboardInterrupt:
                logger.info("\n⛔ Automation stopped by user")
                break
            except Exception as e:
                logger.error(f"Main loop error: {e}")
                time.sleep(300)  # Wait 5 minutes before retrying


if __name__ == "__main__":
    manager = AutomationManager()
    manager.run()
