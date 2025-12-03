# ✅ Railway Scraper Fix - Solution

**Problem:** Instagram blocks cloud IPs - you get 0 posts on Railway  
**Solution:** Scrape locally, upload to cloud (5-minute fix)

---

## What to Do Right Now

### Step 1: Stop the Railway Container
Go to Railway dashboard → Stop the container

### Step 2: Scrape Posts on Your Computer
```bash
cd c:\Users\Asus\Desktop\StructCrew_LeadGen
python 1_scraper/instagram_scraper_pro.py
```

Wait for it to complete (should download 200+ posts to `data/raw_images/`)

### Step 3: Push to GitHub
```bash
git add data/raw_images/
git commit -m "Add scraped posts"
git push origin main
```

### Step 4: Restart Railway
Go to Railway dashboard → Restart the container

Now Railway will:
- ✅ Use the posts you scraped
- ✅ Extract text via OCR (works on cloud)
- ✅ Find emails (works on cloud)
- ✅ Send 500 emails (works on cloud)

---

## Daily Schedule

**You (Local Computer):**
```
02:00 → Run: python 1_scraper/instagram_scraper_pro.py
        Push to GitHub with: git push origin main
```

**Railway (Cloud):**
```
04:00 → Pull from GitHub
        OCR extraction starts
        Email extraction starts
        Email campaign sends 500 emails
```

---

## Why This Works

```
Your Computer:
  ✓ Can scrape Instagram (residential IP)
  ✓ Downloads 200-500 posts daily
  ✓ Pushes to GitHub

Railway Cloud:
  ✓ Gets posts from GitHub
  ✓ Runs OCR (no IP blocking)
  ✓ Extracts emails (no IP blocking)
  ✓ Sends emails (no IP blocking)
```

---

## To Automate Daily Scraping

### Option A: Windows Task Scheduler

Create a `.bat` file in your project:

**File:** `scrape_daily.bat`
```batch
@echo off
cd c:\Users\Asus\Desktop\StructCrew_LeadGen
python 1_scraper/instagram_scraper_pro.py
git add data/raw_images/
git commit -m "Daily scrape - %date%"
git push origin main
pause
```

Then:
1. Open Task Scheduler
2. Create Basic Task
3. Name: "Daily Instagram Scrape"
4. Trigger: Daily at 2:00 AM
5. Action: Run `scrape_daily.bat`

### Option B: Mac/Linux Cron

Create `scrape_daily.sh`:
```bash
#!/bin/bash
cd ~/StructCrew_LeadGen
python 1_scraper/instagram_scraper_pro.py
git add data/raw_images/
git commit -m "Daily scrape"
git push origin main
```

Make executable:
```bash
chmod +x scrape_daily.sh
```

Add to cron:
```bash
crontab -e
# Add line:
0 2 * * * ~/scrape_daily.sh
```

---

## Immediate Test

### Right Now (5 minutes):

1. **On your computer**, run:
```bash
python 1_scraper/instagram_scraper_pro.py
```

Check that it downloads posts (should see 200+ new images)

2. **Push to GitHub:**
```bash
git add data/raw_images/
git commit -m "Test posts"
git push origin main
```

3. **On Railway**, restart the container

4. **Check Railway logs** in 1 hour

Should now see:
- ✅ OCR processing posts
- ✅ Finding emails
- ✅ Sending emails

---

## You're Set!

Once you run the scraper locally and push once, Railway will handle the rest (OCR + emails).

Then just schedule daily scraping on your computer using Task Scheduler/Cron, and it's fully automated.

**Total time to fix:** 5 minutes  
**Results in:** 1 hour (for OCR/email processing)

---

Read: `FIX_RAILWAY_SCRAPER.md` for other options and hybrid setup details.
