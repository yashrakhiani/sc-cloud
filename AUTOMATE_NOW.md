# 🚀 Quick Start: Automate 500 Posts + 500 Emails Daily

## TL;DR - Get Running in 15 Minutes

### 1. Update Your `.env` File
```bash
# Copy template
copy .env.template .env

# Edit with your credentials (notepad .env):
INSTAGRAM_LOGIN_USER=your_username
INSTAGRAM_LOGIN_PASS=your_password
FROM_EMAIL=your-email@gmail.com
GMAIL_APP_PASSWORD=your_app_password
CLAUDE_API_KEY=your_key
```

### 2. Test Locally (5 minutes)
```bash
# Install/update dependencies
pip install -r requirements.txt
playwright install chromium

# Test the new automation manager
python automation_manager.py
```

This will:
- ✅ Scrape 500 Instagram posts
- ✅ Extract text via OCR
- ✅ Find emails in text
- ✅ Send first batch of emails
- ✅ Log everything to `logs/automation_manager.log`

### 3. Deploy to Cloud (Choose One)

#### Option A: Google Cloud (Free Forever)
```bash
# Go to https://console.cloud.google.com/
# Create e2-micro VM, then:

git clone your-repo
cd structcrew-leadgen
nano .env  # Add credentials

# Create swap (CRITICAL)
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# Run
docker build -t leadgen .
docker run -d --restart always -v $(pwd)/data:/app/data leadgen
docker logs -f
```

#### Option B: Railway (Simplest)
```bash
# 1. Go to https://railway.app
# 2. New Project → Deploy from GitHub
# 3. Select your repo
# 4. Add env vars
# 5. Deploy ✓
```

#### Option C: Render
```bash
# 1. Go to https://render.com
# 2. New Web Service → GitHub
# 3. Build: pip install -r requirements.txt
# 4. Start: python automation_manager.py
# 5. Add env vars → Deploy
```

---

## What Happens Each Day

```
2:00 AM UTC  → Scraper downloads 500 posts
4:00 AM UTC  → OCR extracts text from images
5:00 AM UTC  → Email extraction builds database
9:00 AM UTC  → Sends 500 emails (+ full pipeline)
```

**All automated. Nothing to do manually.**

---

## Monitor Progress

```bash
# Check latest status
cat logs/automation_manager.log | tail -50

# See today's results
cat data/automation_state.json

# Count emails sent
sqlite3 data/leads.db "SELECT COUNT(*) FROM emails WHERE status='sent' AND date(sent_at)=date('now')"

# Count posts
sqlite3 data/leads.db "SELECT COUNT(*) FROM raw_posts WHERE date(created_at)=date('now')"
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Instagram blocks scraper | Increase delays in .env: `SCROLL_DELAY=5,10` |
| Emails not sending | Verify Gmail app password, check quota |
| Out of memory error | Add swap file (Google Cloud) or upgrade instance |
| Low email delivery | Warm up gradually: 50→100→200→500/day |
| OCR failing | Switch to Tesseract: `USE_CLAUDE=false` |

---

## Costs

- **Google Cloud:** $0/month (free tier)
- **Claude OCR:** $10-30/month (depending on volume)
- **Gmail:** $0-6/month
- **Total:** $10-36/month for fully automated system

---

## Expected Results

**First Week:**
- 3,500 posts downloaded
- 1,400-2,100 emails collected
- ~3,500 emails sent
- 70-175 responses expected

**First Month:**
- 15,000 posts
- 6,000-9,000 emails collected
- ~15,000 emails sent
- 300-750 responses

**First Year:**
- 180,000 posts
- 72,000-108,000 emails
- ~50,000 emails sent
- 1,000-2,500 actual leads

---

## Next: Detailed Setup

Read the full guide: [`CLOUD_AUTOMATION_SETUP.md`](CLOUD_AUTOMATION_SETUP.md)

---

**That's it! Deploy and let it run. 🎯**
