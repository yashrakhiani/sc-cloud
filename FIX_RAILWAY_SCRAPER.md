# 🔧 Fix: Instagram Scraper on Railway

**Problem:** Scraper returns 0 posts on Railway
**Root Cause:** Instagram blocks cloud server IPs
**Solution:** Use pre-downloaded posts OR scrape locally, upload to cloud

---

## Option 1: FASTEST FIX - Scrape Locally, Upload to Cloud (Recommended)

The scraper **cannot work on cloud** because Instagram blocks all cloud IPs. Instead:

### Step 1: Run Scraper on Your Computer
```bash
# On your local machine (NOT Railway)
python 1_scraper/instagram_scraper_pro.py
```

This will download 200-500 posts to `data/raw_images/`

### Step 2: Upload to Railway
```bash
# Upload the raw_images folder to Railway
# Via Railway dashboard: Settings → Storage
# Or via SFTP/Git
```

### Step 3: Railway Continues the Pipeline
```
Your Computer:  Downloads 200 posts ✓
    ↓
Your Computer:  Uploads to Railway ✓
    ↓
Railway Cloud:  OCR extraction ✓
Railway Cloud:  Email finding ✓
Railway Cloud:  Sends 500 emails ✓
```

---

## Option 2: Use Instaloader (Better for Cloud)

Instaloader is more cloud-friendly. Let's use it instead:

### Step 1: Install Instaloader
```bash
pip install instaloader
```

### Step 2: Create Cloud Scraper Script

Create `1_scraper/scraper_cloud.py`:

```python
#!/usr/bin/env python3
"""Cloud-friendly Instagram scraper using Instaloader"""

import instaloader
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv('INSTAGRAM_USERNAME', 'archijobs')
MAX_POSTS = int(os.getenv('MAX_POSTS', 100))  # Limit for cloud
OUTPUT_DIR = Path('data/raw_images')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def scrape_with_instaloader():
    """Scrape using Instaloader"""
    loader = instaloader.Instaloader(
        download_pictures=True,
        download_videos=False,
        download_captions=True,
        save_metadata=False,
        max_connections=1,  # Cloud-safe
        request_timeout=20
    )
    
    try:
        profile = instaloader.Profile.from_username(loader.context, USERNAME)
        
        posts = 0
        for post in profile.get_posts():
            if posts >= MAX_POSTS:
                break
            
            # Download just the image
            loader.download_post(post, target=str(OUTPUT_DIR))
            posts += 1
            
            if posts % 50 == 0:
                print(f"Downloaded {posts} posts...")
        
        print(f"✅ Downloaded {posts} posts")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    scrape_with_instaloader()
```

### Step 3: Use This in Railway

Update `automation_manager.py` to use `scraper_cloud.py` instead:

```python
# In automation_manager.py, change:
subprocess.run(['python', '1_scraper/instagram_scraper_pro.py'])

# To:
subprocess.run(['python', '1_scraper/scraper_cloud.py'])
```

---

## Option 3: Pre-Load Sample Posts (Quickest for Testing)

If you just want to test the pipeline without scraping:

### Step 1: Create Sample Posts Locally
```bash
python 1_scraper/instagram_scraper_pro.py  # Download 50 posts
```

### Step 2: Add to Git
```bash
git add data/raw_images/
git commit -m "Add sample posts for testing"
git push origin main
```

### Step 3: Railway Uses Pre-Loaded Posts
Railway will automatically use these posts for OCR/email extraction testing.

---

## Option 4: Use Bright Data Residential Proxy (Best for Production)

For production, use a residential proxy service:

### Step 1: Get Proxy Credentials
- Service: Bright Data, Smartproxy, or Oxylabs
- Cost: ~$5-10/month
- Sign up and get proxy URL

### Step 2: Update Scraper
```python
# In instagram_scraper_pro.py, add after line 92:
browser = p.chromium.launch(
    headless=HEADLESS,
    proxy="http://username:password@proxy-server:port",  # Your proxy
    args=['--disable-blink-features=AutomationControlled']
)
```

### Step 3: Add to Environment
```bash
# In Railway environment variables:
PROXY_URL=http://user:pass@server:port
```

---

## Recommended: Hybrid Approach

**Best setup for your situation:**

```
Local Computer:
  ├─ Run scraper daily (python 1_scraper/instagram_scraper_pro.py)
  └─ Git push new images (git add data/raw_images && git push)

Railway Cloud:
  ├─ Pulls latest images from Git
  ├─ OCR extraction (Claude Vision)
  ├─ Email extraction
  └─ Sends 500 emails
```

**Why this works:**
- ✅ Scraping from your PC (Instagram won't block)
- ✅ Cloud handles heavy lifting (OCR + email)
- ✅ Low cost (only pay for Railway compute time for OCR/email)
- ✅ Reliable (no cloud IP blocks)

---

## How to Implement Hybrid (5 minutes)

### Step 1: Update automation_manager.py

Add a check to skip scraping on cloud:

```python
def run_scraper(self):
    """Phase 1: Scrape Instagram posts"""
    
    # Skip if running on cloud and images already exist
    if os.getenv('RAILWAY_ENVIRONMENT_NAME'):  # Cloud environment
        image_count = len(list(Path('data/raw_images').glob('*.jpg')))
        if image_count > 100:
            logger.info("⏭️ Skipping scraper (using pre-loaded images from Git)")
            return
    
    # ... rest of scraper code
```

### Step 2: Create Local Scraper Script

```bash
#!/bin/bash
# File: scrape_daily.sh (run on your computer)

cd ~/StructCrew_LeadGen
python 1_scraper/instagram_scraper_pro.py
git add data/raw_images/
git commit -m "Daily scrape: $(date)"
git push origin main
```

### Step 3: Schedule Locally

On your computer, use Task Scheduler (Windows) or Cron (Mac/Linux):

```bash
# Mac/Linux Cron (run daily at 2 AM)
0 2 * * * ~/scrape_daily.sh

# Windows Task Scheduler:
# Task: "Daily Instagram Scrape"
# Trigger: Daily at 02:00
# Action: Run scrape_daily.sh
```

---

## Immediate Fix for Railway

Your current error shows the scraper is running but getting 0 posts. Here's the quick fix:

### Option A: Disable Scraper on Cloud
```bash
# In Railway environment variables, set:
SKIP_SCRAPER=true
```

Then update automation_manager.py:
```python
if os.getenv('SKIP_SCRAPER') == 'true':
    logger.info("⏭️ Scraper disabled (run locally)")
else:
    self.run_scraper()
```

### Option B: Use Cached Posts
Add sample posts to your Git repo:
```bash
# Locally, download some posts:
python 1_scraper/instagram_scraper_pro.py

# Add to Git:
git add data/raw_images/
git commit -m "Add cached posts"
git push

# Now Railway will use these cached posts
```

---

## Complete Solution (30 minutes setup)

1. **Locally:** Run scraper daily
```bash
python 1_scraper/instagram_scraper_pro.py
```

2. **Locally:** Push to GitHub
```bash
git add data/raw_images/
git commit -m "Daily scrape"
git push origin main
```

3. **Railway:** Pulls and processes
- OCR extraction
- Email finding
- Email sending

4. **Schedule:** Use your computer's scheduler

---

## Why Instagram Blocks Cloud

Instagram's anti-bot system blocks:
- ❌ Cloud server IPs (AWS, Google Cloud, Railway, Render, etc.)
- ❌ Data center IPs
- ❌ Rotating IPs
- ✅ Residential IPs (home internet)
- ✅ VPN with residential IPs

**Cloud scrapers don't work.** This is why we use local scraping + cloud processing.

---

## Next Steps

**Right now:**
1. Check which option works for your setup
2. Implement the hybrid approach (recommended)
3. Redeploy to Railway

**Option 1 (Easiest):** Disable scraper on Railway, scrape locally
**Option 2 (Best):** Hybrid - local scraping + cloud processing
**Option 3 (Premium):** Use residential proxy service

I recommend **Option 1 or 2** for your setup.

---

Would you like me to:
1. Update your code to implement the hybrid approach? ✅
2. Create a local scraper scheduler script? ✅
3. Update automation_manager.py to skip cloud scraping? ✅

Let me know which option you prefer!
