# 🖥️ Multi-PC Local Scraping Setup

**Goal:** Run scrapers on multiple home computers → All data syncs to GitHub → Shared database grows daily

---

## How It Works

```
PC #1 (Home)          PC #2 (Office)       PC #3 (Laptop)
  │                      │                    │
  ├─ Scrape 100 posts    ├─ Scrape 100 posts ├─ Scrape 100 posts
  ├─ Push to GitHub      ├─ Push to GitHub   ├─ Push to GitHub
  │                      │                    │
  └──────────┬───────────┴────────────────────┘
             │
             ↓
        Shared GitHub Database
             │
        Total: 500+ posts/day
        Growing daily
        All deduplicated
```

---

## Setup (5 Minutes Per PC)

### Step 1: Clone Repository
```bash
git clone https://github.com/yashrakhiani/sc-cloud.git
cd sc-cloud
```

### Step 2: Run Setup Installer
```bash
python setup_multi_pc.py
```

This will ask:
1. **PC Name** - e.g., "home-pc-1", "office-pc-2"
2. Install dependencies
3. Setup auto-scheduling

### Step 3: That's It!
The scraper will start automatically:
- Runs 5 sessions per day
- Scrapes 100 posts per session
- Deduplicates before adding to database
- Auto-pushes to GitHub every session

---

## Daily Schedule

Each PC runs **5 sessions** throughout the day:

```
00:00 UTC (or your time) → Session 1 (100 posts)
04:00 UTC               → Session 2 (100 posts)
08:00 UTC               → Session 3 (100 posts)
12:00 UTC               → Session 4 (100 posts)
16:00 UTC               → Session 5 (100 posts)
────────────────────────────────────────
                Total: 500 posts
```

**If running on multiple PCs:**
- PC 1: Sessions at 0:00, 4:00, 8:00, 12:00, 16:00 = 500 posts
- PC 2: Sessions at 1:00, 5:00, 9:00, 13:00, 17:00 = 500 posts
- PC 3: Sessions at 2:00, 6:00, 10:00, 14:00, 18:00 = 500 posts

**Total: 1,500 unique posts daily** ✅

---

## Database Deduplication

**Key feature:** No duplicate posts across all PCs

```python
# Every session:
1. Load all existing post URLs from GitHub
2. Check: Is this post already downloaded?
3. If YES → Skip it
4. If NO → Download it
5. Save to database
6. Push to GitHub
```

This means:
- ✅ Multiple PCs can scrape same account
- ✅ No wasted bandwidth on duplicates
- ✅ Database grows efficiently
- ✅ All data synced automatically

---

## File Structure

```
StructCrew_LeadGen/
├── local_scraper_scheduler.py   ← Main scraper orchestrator
├── setup_multi_pc.py             ← Installer script
│
├── data/
│   ├── raw_images/              ← Downloaded posts (grows daily)
│   ├── scraped_urls.json         ← All URLs (for deduplication)
│   ├── local_scraper_state.json  ← Progress tracking
│   └── leads.db                  ← Database
│
├── logs/
│   ├── local_scraper.log         ← Detailed logs per session
│   └── cron.log / launchd.log    ← Scheduler logs
│
└── 1_scraper/
    └── instagram_scraper_pro.py  ← Playwright-based scraper
```

---

## Multi-PC Workflow

### PC #1 (Home Computer)
```bash
# One-time setup
git clone https://github.com/yashrakhiani/sc-cloud.git
cd sc-cloud
python setup_multi_pc.py
# Choose PC name: "home-pc-1"
# Auto-scheduled to run every 4 hours
```

### PC #2 (Office Computer)
```bash
# Same setup
git clone https://github.com/yashrakhiani/sc-cloud.git
cd sc-cloud
python setup_multi_pc.py
# Choose PC name: "office-pc-2"
# Auto-scheduled (offset times to avoid conflicts)
```

### PC #3 (Laptop)
```bash
# Same setup
git clone https://github.com/yashrakhiani/sc-cloud.git
cd sc-cloud
python setup_multi_pc.py
# Choose PC name: "laptop-pc-3"
# Auto-scheduled
```

**Result:** Each PC scrapes 500 posts/day, all synced to shared GitHub database

---

## What Gets Synced to GitHub

```
Each session commits:
- ✅ New images (raw_images/)
- ✅ Updated state file (local_scraper_state.json)
- ✅ Updated dedup list (scraped_urls.json)
- ❌ NOT: full database (too large, can be generated)

Commit message shows:
"Local scrape: 87 posts (home-pc-1) - 2025-12-03 08:15"
```

---

## Monitoring Progress

### Check Real-Time Logs
```bash
# On any PC
tail -f logs/local_scraper.log
```

You'll see:
```
2025-12-03 08:00:15 - INFO - 📱 SCRAPING SESSION 1/5 - home-pc-1
2025-12-03 08:00:15 - INFO - Target: 100 posts
2025-12-03 08:20:45 - INFO - ✅ Session 1 complete
2025-12-03 08:20:45 - INFO - New images: 87
2025-12-03 08:20:45 - INFO - Today's total: 87/500
2025-12-03 08:20:50 - INFO - 🔄 Syncing to GitHub...
2025-12-03 08:21:15 - INFO - ✅ GitHub sync complete
```

### Check GitHub Activity
```bash
# View commits from all PCs
git log --oneline | head -20

# See posts added by each PC
git log --grep="Local scrape"
```

### Check Database Growth
```bash
# Count total unique posts
sqlite3 data/leads.db "SELECT COUNT(*) FROM raw_posts"

# See when last post was added
sqlite3 data/leads.db "SELECT MAX(created_at) FROM raw_posts"

# Count by PC
sqlite3 data/leads.db "SELECT pc_name, COUNT(*) FROM raw_posts GROUP BY pc_name"
```

---

## Troubleshooting

### Scheduler Not Running
```bash
# Test manually
python local_scraper_scheduler.py

# Should show:
# 🚀 Local Multi-PC Scraper Scheduler - home-pc-1
# 🔄 Entering scheduling loop...
```

### Git Push Failing
```bash
# Check credentials
git status

# Common fix (Windows)
git config --global credential.helper wincred

# Common fix (Mac)
git config --global credential.helper osxkeychain

# Or use SSH keys (more secure)
git config --global core.sshCommand "ssh -i ~/.ssh/id_rsa"
```

### Duplicate Posts
```bash
# Check dedup file
cat data/scraped_urls.json

# If duplicates exist, clean:
python -c "
import json
urls = json.load(open('data/scraped_urls.json'))
urls = list(set(urls))
json.dump(urls, open('data/scraped_urls.json', 'w'))
"
```

### Low Post Count
```bash
# Check if Instagram blocked the PC
# Logs will show: "403 Forbidden"

# Solutions:
# 1. Use VPN (best)
# 2. Scrape less frequently (increase intervals)
# 3. Use residential proxy service ($5-10/month)
```

---

## Advanced: Customize Schedule

### Change Post Count Per Session
```bash
# In local_scraper_scheduler.py
self.config = {
    'DAILY_TARGET': 1000,           # Up to 1000 posts/day
    'POSTS_PER_SESSION': 200,       # 200 posts/session
    'SESSIONS_PER_DAY': 5,          # 5 sessions
}
```

### Change Session Times
```bash
# In local_scraper_scheduler.py
hours = [0, 4, 8, 12, 16]           # Change to: [1, 5, 9, 13, 17]
```

### Skip Sync on Every Session
```bash
# Reduce GitHub API calls
# In run_scraping_session():
if self.state['sessions_completed'] % 2 == 0:  # Sync every 2 sessions
    self.sync_to_github()
```

---

## Expected Results

### First Day
```
PC Home:     500 posts
PC Office:   500 posts  
PC Laptop:   500 posts
─────────────────────
Total:       1,500 posts
Unique:      1,400-1,500 (some overlap removed)
```

### First Week
```
Posts:       10,000+
Emails:      4,000-6,000 (40-60% extraction rate)
Database:    Growing by 1,500-2,000/day
```

### First Month
```
Posts:       45,000+
Emails:      18,000-27,000
GitHub:      50+ commits (one per session)
Duplicates:  <1% (deduplication working)
```

---

## Security Notes

- ✅ `.gitignore` includes credentials
- ✅ API keys stay in `.env` (not pushed)
- ✅ Each PC has unique identity
- ⚠️ Keep `.env` file private
- ⚠️ Don't commit credentials to GitHub

---

## Expanding to More PCs

Add as many PCs as you want:

```bash
# PC #4
python setup_multi_pc.py  # Name: "garage-pc-4"

# PC #5
python setup_multi_pc.py  # Name: "backup-pc-5"

# etc...
```

Each adds 500 posts/day to shared database.

**With 3 PCs:** 1,500 posts/day = 45,000/month  
**With 5 PCs:** 2,500 posts/day = 75,000/month  
**With 10 PCs:** 5,000 posts/day = 150,000/month

---

## Next: Process the Posts

Once scraping runs:

```bash
# On cloud (Railway), it will:
1. Pull new posts from GitHub
2. Run OCR extraction
3. Find emails
4. Send campaign emails

# OR process locally:
python 2_ocr/process_images_pro.py
python 3_email_extractor/extract_emails_pro.py
```

---

## Summary

✅ **Setup:** 5 minutes per PC  
✅ **Scheduling:** Automatic via Task Scheduler/Cron  
✅ **Deduplication:** All URLs tracked globally  
✅ **Sync:** Auto-push to GitHub after each session  
✅ **Growth:** 500 posts/day per PC  
✅ **Scalable:** Add more PCs anytime  

**One command to install everywhere:**
```bash
python setup_multi_pc.py
```

That's it! 🚀
