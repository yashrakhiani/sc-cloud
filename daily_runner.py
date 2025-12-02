import time
import subprocess
import os
import schedule
import logging
from datetime import datetime
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/automation.log'),
        logging.StreamHandler()
    ]
)

def run_pipeline():
    """Runs the OCR + extraction + email pipeline (cloud-only)."""
    logging.info("🚀 STARTING DAILY PIPELINE RUN (NO SCRAPING IN CLOUD)")

    # 1. OCR Processing
    logging.info("🔍 Phase 2: Running OCR...")
    try:
        subprocess.run(["python", "2_ocr/process_images_pro.py"], check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"OCR failed: {e}")
    
    # 2. Email Extraction
    logging.info("⛏️ Phase 3: Extracting Emails...")
    try:
        subprocess.run(["python", "3_email_extractor/extract_emails_pro.py"], check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Extraction failed: {e}")

    # 3. Send Emails (with progressive scaling)
    logging.info("📧 Phase 4: Sending Emails...")
    
    # Progressive Scaling Logic
    current_limit = int(os.getenv('DAILY_EMAIL_LIMIT', 10))
    max_limit = 500
    
    # Increase limit by 10 for tomorrow (if under max)
    if current_limit < max_limit:
        new_limit = min(current_limit + 10, max_limit)
        update_env_limit(new_limit)
        logging.info(f"📈 Increasing daily limit from {current_limit} to {new_limit} for next run.")
    
    try:
        # Run in live mode
        subprocess.run(["python", "send_emails_simple.py", "--live", "--auto"], check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Email sending failed: {e}")

    logging.info("✅ DAILY PIPELINE COMPLETE. Sleeping for 24 hours...")

def update_env_limit(new_limit):
    """Updates the .env file with the new limit"""
    env_path = Path('.env')
    if not env_path.exists():
        return
        
    lines = env_path.read_text().splitlines()
    new_lines = []
    updated = False
    
    for line in lines:
        if line.startswith('DAILY_EMAIL_LIMIT='):
            new_lines.append(f'DAILY_EMAIL_LIMIT={new_limit}')
            updated = True
        else:
            new_lines.append(line)
    
    if not updated:
        new_lines.append(f'DAILY_EMAIL_LIMIT={new_limit}')
        
    env_path.write_text('\n'.join(new_lines))

if __name__ == "__main__":
    print("="*60)
    print("🤖 StructCrew Cloud Automation Agent")
    print("="*60)
    print("Status: RUNNING")
    print("Schedule: Daily at 09:00 UTC (OCR + extract + emails only)")
    print("="*60)
    
    # Run once immediately on startup (pipeline only)
    run_pipeline()
    
    # Schedule daily full pipeline (OCR + extract + email)
    schedule.every().day.at("09:00").do(run_pipeline)
    
    while True:
        schedule.run_pending()
        time.sleep(60)
