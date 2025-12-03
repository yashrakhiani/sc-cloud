# ✅ Deployment Checklist

Complete this checklist before deploying to cloud.

---

## Pre-Deployment (Do These First)

### 1. Credentials Ready
- [ ] Instagram username
- [ ] Instagram password
- [ ] Gmail address
- [ ] Gmail app password (16 characters)
- [ ] Claude API key
- [ ] (Optional) Gemini API key

**How to get credentials:**

**Gmail App Password:**
1. Go to myaccount.google.com/security
2. Turn on 2-Factor Authentication (if not already)
3. Create App Password (for Python)
4. Copy the 16-character code

**Claude API Key:**
1. Go to console.anthropic.com
2. API Keys → Create new key
3. Copy the key

### 2. Test Locally
- [ ] Python installed (`python --version`)
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Playwright installed (`playwright install chromium`)
- [ ] `.env` file created and filled in
- [ ] Local test passed (`python automation_manager.py` runs without crashing)

### 3. Code Ready
- [ ] Git repository set up
- [ ] `automation_manager.py` committed
- [ ] `Dockerfile` updated
- [ ] `.env.template` contains all required keys
- [ ] All documentation in place

---

## Choose Your Cloud Platform

### Platform A: Google Cloud
**Cost:** $0/month (free tier)  
**Difficulty:** Medium (need SSH, Docker)  
**Time:** 15-20 minutes

**Requirements:**
- [ ] Google account
- [ ] Google Cloud enabled (console.cloud.google.com)
- [ ] Credit card (for free tier)

**Before deploying:**
- [ ] Understand swap memory (critical!)
- [ ] Read "Setup Swap Memory" in DEPLOY_CLOUD_NOW.md
- [ ] Have SSH client ready

### Platform B: Railway
**Cost:** $5-15/month  
**Difficulty:** Easy (GitHub connected)  
**Time:** 5 minutes

**Requirements:**
- [ ] GitHub account with repo
- [ ] Railway account (railway.app)

**Before deploying:**
- [ ] Repository is public or Railway has access
- [ ] All environment variables documented

### Platform C: Render
**Cost:** $7+/month  
**Difficulty:** Easy (web form)  
**Time:** 10 minutes

**Requirements:**
- [ ] GitHub account with repo
- [ ] Render account (render.com)

**Before deploying:**
- [ ] Repository is connected
- [ ] All environment variables ready

---

## Configuration Checklist

### .env File
- [ ] `INSTAGRAM_LOGIN_USER=your_username`
- [ ] `INSTAGRAM_LOGIN_PASS=your_password`
- [ ] `INSTAGRAM_USERNAME=archijobs` (or your target)
- [ ] `FROM_EMAIL=your-email@gmail.com`
- [ ] `GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx` (16 chars)
- [ ] `CLAUDE_API_KEY=sk-ant-...` (if using Claude)
- [ ] `GEMINI_API_KEY=AIzaSyD...` (if using Gemini)
- [ ] `HEADLESS=true`
- [ ] `MAX_POSTS=500`
- [ ] `DAILY_EMAIL_LIMIT=500`
- [ ] `USE_CLAUDE=true`

### Optional Configuration
- [ ] `INSTAGRAM_USERNAMES=account1,account2` (multiple accounts)
- [ ] `SCROLL_DELAY=3,7` (anti-ban delays)
- [ ] `RATE_LIMIT_DELAY=1` (OCR delays)
- [ ] `VALIDATE_EMAILS=true` (email validation)

---

## Deployment Steps (Per Platform)

### For Google Cloud Users

1. **Create Instance**
   - [ ] Region: us-central1 (must be free tier region)
   - [ ] Machine type: e2-micro
   - [ ] Boot disk: Ubuntu 22.04 LTS, 30GB
   - [ ] Firewall: Allow HTTP/HTTPS
   - [ ] Click Create

2. **SSH Setup**
   - [ ] Instance created (wait ~1 min)
   - [ ] Click SSH button
   - [ ] Browser window opens

3. **Create Swap Memory (CRITICAL)**
   ```bash
   sudo fallocate -l 2G /swapfile
   sudo chmod 600 /swapfile
   sudo mkswap /swapfile
   sudo swapon /swapfile
   echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
   ```
   - [ ] All commands run without errors
   - [ ] `free -h` shows swap file

4. **Install Dependencies**
   ```bash
   sudo apt-get update
   sudo apt-get install -y docker.io git
   sudo usermod -aG docker $USER
   newgrp docker
   ```
   - [ ] Docker installed (`docker --version`)
   - [ ] Git installed (`git --version`)

5. **Deploy Application**
   ```bash
   git clone https://github.com/YOUR_USERNAME/structcrew-leadgen
   cd structcrew-leadgen
   nano .env  # Paste your credentials
   docker build -t leadgen .
   docker run -d --name automation --restart unless-stopped -v $(pwd)/data:/app/data leadgen
   ```
   - [ ] Clone successful
   - [ ] .env file created and saved
   - [ ] Docker build completed
   - [ ] Container running (`docker ps`)

6. **Verify**
   ```bash
   docker logs -f automation
   ```
   - [ ] See "STARTING DAILY AUTOMATION PIPELINE"
   - [ ] No errors in first few lines
   - [ ] Let it run for 1-2 minutes, then Ctrl+C

### For Railway Users

1. **Create Account**
   - [ ] Account created at railway.app
   - [ ] GitHub authorized

2. **Create Project**
   - [ ] Click New Project
   - [ ] Select "Deploy from GitHub"
   - [ ] Select your repository

3. **Configure**
   - [ ] Select branch (usually `main`)
   - [ ] Build command auto-filled
   - [ ] Start command auto-filled

4. **Add Environment Variables**
   - [ ] Click Variables tab
   - [ ] Paste all variables from `.env`
   - [ ] All 12+ variables entered

5. **Deploy**
   - [ ] Click Deploy
   - [ ] Wait 3-5 minutes for build
   - [ ] Check Logs tab

6. **Verify**
   - [ ] Logs show successful build
   - [ ] "STARTING DAILY AUTOMATION PIPELINE" appears
   - [ ] No error messages

### For Render Users

1. **Create Account**
   - [ ] Account created at render.com
   - [ ] GitHub authorized

2. **Create Service**
   - [ ] Click New +
   - [ ] Select Web Service
   - [ ] Select GitHub repo

3. **Configure**
   - [ ] Build command: `pip install -r requirements.txt`
   - [ ] Start command: `python automation_manager.py`
   - [ ] Environment: Python 3

4. **Add Variables**
   - [ ] Click Environment
   - [ ] Add all variables from `.env`
   - [ ] All 12+ variables entered

5. **Deploy**
   - [ ] Click Deploy
   - [ ] Watch build progress
   - [ ] Takes 5-10 minutes

6. **Verify**
   - [ ] Check Logs
   - [ ] "STARTING DAILY AUTOMATION PIPELINE"
   - [ ] No errors

---

## Post-Deployment Verification

### Immediate (First 5 minutes)
- [ ] No error messages in logs
- [ ] All 4 phases started:
  - [ ] PHASE 1: INSTAGRAM SCRAPER
  - [ ] PHASE 2: OCR TEXT EXTRACTION
  - [ ] PHASE 3: EMAIL EXTRACTION
  - [ ] PHASE 4: EMAIL CAMPAIGN
- [ ] "DAILY PIPELINE COMPLETE" message

### After 1 Hour
- [ ] Check logs for completion
- [ ] Check for errors

### After 24 Hours
- [ ] [ ] New images in `data/raw_images/` (should be 500+)
- [ ] [ ] Check database: `SELECT COUNT(*) FROM raw_posts` (should be 500+)
- [ ] [ ] Check emails: `SELECT COUNT(*) FROM emails` (should be 200-300+)
- [ ] [ ] Check sent: `SELECT COUNT(*) FROM emails WHERE status='sent'` (should be 500+)
- [ ] [ ] No errors in logs

### After 7 Days
- [ ] [ ] Scraper still working (no 403 blocks)
- [ ] [ ] 3,500+ posts accumulated
- [ ] [ ] 1,400-2,100+ emails collected
- [ ] [ ] 3,500+ emails sent
- [ ] [ ] Email responses starting to come in

---

## Monitoring Setup (Optional)

### Daily Monitoring
- [ ] Set phone reminder to check logs daily
- [ ] Quick command: `tail -10 logs/automation_manager.log`

### Weekly Checks
- [ ] Email stats: `SELECT COUNT(*) FROM emails WHERE date(sent_at) >= date('now', '-7 days')`
- [ ] Bounce rate check
- [ ] Response rate check

### Monthly Analysis
- [ ] Full metrics review
- [ ] Cost analysis
- [ ] Optimization discussion

---

## Troubleshooting Pre-Flight

Before deployment, make sure:

- [ ] Instagram login works (test manually)
- [ ] Gmail app password is correct (16 characters with spaces)
- [ ] Claude API key is valid (test with curl)
- [ ] All `.env` variables are present
- [ ] No typos in credentials
- [ ] Python environment has all dependencies

**Test locally first!**
```bash
python automation_manager.py
```

Should complete full cycle without errors.

---

## What to Do If Something Breaks

### Container Won't Start
1. [ ] Check logs: `docker logs automation`
2. [ ] Common causes:
   - [ ] Missing .env variable → Add it
   - [ ] Wrong credentials → Fix and restart
   - [ ] Out of memory → Create swap file (Google Cloud)
   - [ ] Dependency error → Rebuild image

### No Data After 24 Hours
1. [ ] Check if container is running
2. [ ] Check logs for errors
3. [ ] Verify Instagram credentials
4. [ ] Check if Instagram blocked the account

### Emails Not Sending
1. [ ] Verify Gmail app password
2. [ ] Check Gmail API quota
3. [ ] Verify FROM_EMAIL setting
4. [ ] Check database for pending emails

### Out of Memory (Google Cloud)
1. [ ] Was swap file created?
2. [ ] If not, create it immediately
3. [ ] Restart container

---

## Success Indicators

You'll know everything is working when:

✅ **24 hours in:**
- Logs show all 4 phases completing daily
- 500+ new images in raw_images/
- 200-300+ new emails in database
- 500 emails marked as sent

✅ **1 week in:**
- 3,500+ posts downloaded
- 1,400-2,100+ unique emails found
- 3,500+ emails sent
- First responses coming in

✅ **Ongoing:**
- Database growing consistently
- No errors in logs
- Response rate 2-5%
- Bounce rate <5%

---

## Final Checklist

- [ ] All credentials collected
- [ ] Local test passed
- [ ] Platform chosen (Google Cloud / Railway / Render)
- [ ] Ready to follow deployment steps
- [ ] Have 30 minutes available for deployment
- [ ] Saved this checklist for reference

---

## You're Ready! 🚀

Follow these steps in order:

1. **Gather credentials** (5 min)
2. **Test locally** (10 min)
3. **Choose platform** (2 min)
4. **Deploy** (15-30 min per platform)
5. **Verify in 24 hours** (5 min)

**Total time: 45 minutes - then it runs itself!**

---

**✨ Good luck with deployment! You've got this! ✨**
