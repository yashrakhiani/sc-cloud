# ☁️ Deploy Cloud Automation - Step by Step

## Pre-Deployment Checklist

- [ ] Updated `.env` file with all credentials
- [ ] Tested locally: `python automation_manager.py`
- [ ] Verified Instagram login works
- [ ] Verified Claude/Gemini API keys work
- [ ] Gmail app password generated
- [ ] Git repository up to date

---

## CHOOSE YOUR DEPLOYMENT METHOD

---

# 🔵 METHOD 1: Railway.app (EASIEST - Recommended)

**Cost:** $5-15/month  
**Setup Time:** 5 minutes  
**Maintenance:** Almost none

### Step 1: Create Railway Account
1. Go to https://railway.app
2. Sign up with GitHub
3. Create new project

### Step 2: Deploy from GitHub
1. Click **New Project** → **Deploy from GitHub**
2. Authorize and select your repository
3. Select the branch (usually `main`)

### Step 3: Add Environment Variables
In Railway dashboard, go to **Variables** tab:

```
INSTAGRAM_LOGIN_USER=your_username
INSTAGRAM_LOGIN_PASS=your_password
INSTAGRAM_USERNAME=archijobs
FROM_EMAIL=your-email@gmail.com
GMAIL_APP_PASSWORD=your_app_password
CLAUDE_API_KEY=sk-ant-...
GEMINI_API_KEY=AIzaSyD...
HEADLESS=true
MAX_POSTS=500
DAILY_EMAIL_LIMIT=500
USE_CLAUDE=true
```

### Step 4: Deploy
1. Click **Deploy**
2. Wait 3-5 minutes for build
3. Check **Logs** for "STARTING DAILY AUTOMATION PIPELINE"

### Step 5: Monitor
- **Logs:** Available in dashboard
- **Status:** Green = running
- **Restart:** Automatic on errors

---

# 🟢 METHOD 2: Google Cloud (FREE - Recommended for long-term)

**Cost:** $0/month (free tier forever)  
**Setup Time:** 15 minutes  
**Maintenance:** Minimal

### Step 1: Create Google Cloud Account
1. Go to https://console.cloud.google.com/
2. Create project (name: `structcrew-leadgen`)
3. Enable billing (won't charge if under free tier limits)

### Step 2: Create VM Instance
1. **Compute Engine** → **VM Instances** → **Create**

**Settings:**
```
Region: us-central1 (must be one of: us-central1, us-west1, us-east1)
Zone: us-central1-a
Machine type: e2-micro (2 vCPU, 1 GB)
Boot disk: Ubuntu 22.04 LTS
Boot disk size: 30GB (Standard persistent disk)
Firewall: Allow HTTP & HTTPS
```

2. Click **Create**
3. Wait 1-2 minutes for instance to start

### Step 3: Connect via SSH
1. Click **SSH** button next to your instance
2. New browser window opens

### Step 4: Setup Swap Memory (CRITICAL!)
```bash
# Create 2GB swap file
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab

# Verify
free -h
```

### Step 5: Install Docker & Dependencies
```bash
sudo apt-get update
sudo apt-get install -y docker.io git
sudo usermod -aG docker $USER
newgrp docker
```

### Step 6: Clone Repository
```bash
git clone https://github.com/YOUR_USERNAME/structcrew-leadgen.git
cd structcrew-leadgen
```

### Step 7: Create .env File
```bash
nano .env
```

Paste your environment variables:
```
INSTAGRAM_LOGIN_USER=your_username
INSTAGRAM_LOGIN_PASS=your_password
INSTAGRAM_USERNAME=archijobs
FROM_EMAIL=your-email@gmail.com
GMAIL_APP_PASSWORD=your_app_password
CLAUDE_API_KEY=sk-ant-...
GEMINI_API_KEY=AIzaSyD...
HEADLESS=true
MAX_POSTS=500
DAILY_EMAIL_LIMIT=500
USE_CLAUDE=true
```

Press `Ctrl+X`, then `Y`, then `Enter` to save.

### Step 8: Build & Run Docker
```bash
docker build -t structcrew-leadgen .
docker run -d \
  --name automation \
  --restart unless-stopped \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/logs:/app/logs \
  -e PYTHONUNBUFFERED=1 \
  structcrew-leadgen
```

### Step 9: Verify It's Running
```bash
# Check container is running
docker ps

# View logs
docker logs -f automation
```

You should see:
```
🚀 STARTING DAILY AUTOMATION PIPELINE
🌍 PHASE 1: INSTAGRAM SCRAPER (500 posts)
```

### Step 10: Monitor Long-term
```bash
# Check logs anytime
docker logs automation | tail -50

# Check specific date
docker logs automation | grep "2025-12-04"

# View automation state
cat data/automation_state.json

# Count emails sent today
sqlite3 data/leads.db "SELECT COUNT(*) FROM emails WHERE date(sent_at)=date('now')"
```

**To stop/restart:**
```bash
docker stop automation
docker start automation
docker restart automation
```

---

# 🟡 METHOD 3: Render (RELIABLE - Not free but affordable)

**Cost:** $7/month minimum  
**Setup Time:** 10 minutes  
**Maintenance:** Minimal

### Step 1: Create Render Account
1. Go to https://render.com
2. Sign up with GitHub
3. Create new web service

### Step 2: Deploy from GitHub
1. Click **New +** → **Web Service**
2. Connect GitHub account
3. Select repository
4. Select branch (`main`)

### Step 3: Configure Service
```
Name: structcrew-leadgen
Environment: Python 3
Region: Oregon (us-west)
Build Command: pip install -r requirements.txt
Start Command: python automation_manager.py
```

### Step 4: Add Environment Variables
Go to **Environment** section and add:
```
INSTAGRAM_LOGIN_USER=...
INSTAGRAM_LOGIN_PASS=...
FROM_EMAIL=...
GMAIL_APP_PASSWORD=...
CLAUDE_API_KEY=...
(etc - same as above)
```

### Step 5: Deploy
1. Click **Deploy**
2. Watch build progress
3. Check **Logs** when complete

### Step 6: Monitor
- **Logs:** In dashboard
- **Restart:** Automatic
- **Update:** Push to GitHub, auto-redeploy

---

# ✅ POST-DEPLOYMENT VERIFICATION

## Test That Everything Works

### 1. Check Logs (First 5 minutes)
```
PHASE 1: INSTAGRAM SCRAPER ✓
PHASE 2: OCR TEXT EXTRACTION ✓
PHASE 3: EMAIL EXTRACTION ✓
PHASE 4: EMAIL CAMPAIGN ✓
```

### 2. Verify Schedule Is Running
```
08:00 UTC: Scraper starts
10:00 UTC: OCR begins
... (check at scheduled times)
```

### 3. Check Database
```bash
# SSH/console, then:
sqlite3 data/leads.db "SELECT COUNT(*) FROM raw_posts"
sqlite3 data/leads.db "SELECT COUNT(*) FROM emails"
```

Should see increasing counts each day.

### 4. Monitor First Week
Daily checklist:
- [ ] Check logs for errors
- [ ] Verify emails sent count increasing
- [ ] Confirm no spam complaints
- [ ] Monitor Instagram blocking status

---

# 🔧 TROUBLESHOOTING

## Container Crashes / Out of Memory
**Google Cloud:** Make sure swap file is created (Step 4)
**Railway/Render:** Try next highest tier

## Instagram Blocks Requests
```bash
# Edit .env and increase delays:
SCROLL_DELAY=5,15  # (was 3,7)
```

## Gmail Quota Exceeded
- Free Gmail: Limited to 100/day
- Solution: Use Google Workspace ($6/month) = 1,500/day

## Docker Build Fails
```bash
# Check disk space
df -h

# Clear Docker cache
docker system prune -a
```

## Can't Connect via SSH (Google Cloud)
1. Check firewall settings
2. Make sure SSH port (22) is open
3. Generate new SSH key in Cloud Console

---

# 📊 EXPECTED DAILY OUTPUT

After 24 hours, you should see:
- ✅ ~500 new images in `data/raw_images/`
- ✅ ~300-400 extracted texts in `data/extracted_text/`
- ✅ ~200-300 new emails in database
- ✅ ~500 emails sent
- ✅ Detailed logs in `logs/automation_manager.log`

---

# 🔄 DAILY MAINTENANCE

Nothing! It's automated. But optional:

```bash
# Daily (takes 10 seconds):
docker logs automation | tail -50  # Check for errors

# Weekly (takes 1 minute):
sqlite3 data/leads.db "SELECT status, COUNT(*) FROM emails GROUP BY status"

# Monthly (takes 5 minutes):
# Review logs for optimization opportunities
```

---

# 💡 NEXT STEPS

1. **Deployed?** Great! Check logs for 24 hours
2. **All working?** Monitor first week for issues
3. **Any problems?** See Troubleshooting section above
4. **Want to optimize?** Read CLOUD_AUTOMATION_SETUP.md

---

# 📞 SUPPORT

**Logs Location:**
- Railway: Dashboard → Logs
- Google Cloud: `docker logs automation`
- Render: Dashboard → Logs

**Common Issues:**
- `Error: Instagram blocked`: Increase delays, use VPN
- `Gmail quota exceeded`: Upgrade to Workspace or use Sendgrid
- `Out of memory`: Add swap or upgrade instance

---

**✨ Done! Your automation is now running 24/7 in the cloud. 🚀**
