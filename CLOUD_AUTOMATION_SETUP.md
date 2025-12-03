# ☁️ Cloud Automation Setup: 500 Posts + 500 Emails Daily

## Overview

Complete automation pipeline that:
- ✅ Downloads 500 unique Instagram posts daily (off-peak hours)
- ✅ Extracts text via OCR
- ✅ Processes emails from extracted text
- ✅ Sends 500 emails daily
- ✅ Runs entirely in background on cloud

**Timeline:** ~6-8 hours total per day (automated)

---

## Architecture

```
02:00 UTC: Scraper starts (500 posts, 2-3 hours)
    ↓
04:00 UTC: OCR text extraction begins (1-2 hours)
    ↓
05:00 UTC: Email extraction starts (30 mins)
    ↓
09:00 UTC: Full pipeline + Email campaign (500 emails sent)
    ↓
Repeat next day
```

---

## Step 1: Choose Your Cloud Provider

### Option A: Google Cloud (Recommended - Free Tier)
- ✅ 1 e2-micro VM (always free)
- ✅ 1GB storage (free tier)
- ✅ Easiest setup

### Option B: Railway.app
- ✅ $5/month, pay-as-you-go
- ✅ Deploy from GitHub in 3 clicks
- ✅ Built-in logging

### Option C: Render
- ✅ $7/month standard plan
- ✅ Good uptime (99.9%)
- ✅ Auto-deploy from GitHub

---

## Step 2: Prepare Your Environment

### Update render.yaml
```yaml
services:
  - type: worker
    name: structcrew-leadgen
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python automation_manager.py
    envVars:
      - key: INSTAGRAM_USERNAME
        value: archijobs
      - key: INSTAGRAM_LOGIN_USER
        sync: false
      - key: INSTAGRAM_LOGIN_PASS
        sync: false
      - key: CLAUDE_API_KEY
        sync: false
      - key: FROM_EMAIL
        value: your-email@gmail.com
      - key: GMAIL_APP_PASSWORD
        sync: false
      - key: HEADLESS
        value: "true"
      - key: MAX_POSTS
        value: "500"
      - key: DAILY_EMAIL_LIMIT
        value: "500"
```

### Required .env Variables
```
# Instagram
INSTAGRAM_LOGIN_USER=your_ig_username
INSTAGRAM_LOGIN_PASS=your_ig_password
INSTAGRAM_USERNAME=archijobs

# Email Sending
FROM_EMAIL=your-email@gmail.com
GMAIL_APP_PASSWORD=your-16-char-app-password

# API Keys
CLAUDE_API_KEY=sk-ant-...
GEMINI_API_KEY=AIzaSyD...  # Optional, fallback

# Configuration
HEADLESS=true
MAX_POSTS=500
DAILY_EMAIL_LIMIT=500
USE_CLAUDE=true
```

---

## Step 3: Deploy to Cloud

### Google Cloud (Free Tier)

1. **Create VM instance:**
   ```
   Console: https://console.cloud.google.com/
   Compute Engine → VM Instances → Create
   
   Settings:
   - Region: us-central1 (free tier)
   - Machine: e2-micro
   - Boot Disk: Ubuntu 22.04 LTS, 30GB
   - Firewall: Allow HTTP/HTTPS
   ```

2. **Setup swap memory (CRITICAL for 1GB RAM):**
   ```bash
   ssh into instance, then:
   
   sudo fallocate -l 2G /swapfile
   sudo chmod 600 /swapfile
   sudo mkswap /swapfile
   sudo swapon /swapfile
   echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
   ```

3. **Install dependencies:**
   ```bash
   sudo apt-get update
   sudo apt-get install -y python3-pip git docker.io
   sudo usermod -aG docker $USER
   ```

4. **Clone and setup:**
   ```bash
   git clone https://github.com/your-repo/structcrew-leadgen.git
   cd structcrew-leadgen
   cp .env.template .env
   # Edit .env with your credentials
   nano .env
   ```

5. **Run with Docker:**
   ```bash
   docker build -t leadgen .
   docker run -d --name automation --restart always \
     -v $(pwd)/data:/app/data \
     -v $(pwd)/logs:/app/logs \
     leadgen
   ```

6. **Monitor:**
   ```bash
   docker logs -f automation
   cat logs/automation_manager.log
   ```

### Railway.app (Easiest)

1. Go to https://railway.app
2. New Project → Deploy from GitHub
3. Select your repository
4. Add environment variables (same as .env)
5. Deploy! (automatic from GitHub)
6. Logs visible in dashboard

### Render (Manual but Reliable)

1. Go to https://render.com
2. New → Web Service
3. Connect GitHub repository
4. Set environment variables
5. Deploy
6. View logs in dashboard

---

## Step 4: Verify Automation

### Check Status
```bash
# View logs
cat logs/automation_manager.log

# Check last run
cat data/automation_state.json

# Count emails sent
sqlite3 data/leads.db "SELECT COUNT(*) FROM emails WHERE status='sent' AND date(sent_at)=date('now')"

# Count posts
sqlite3 data/leads.db "SELECT COUNT(*) FROM raw_posts WHERE date(created_at)=date('now')"
```

### Monitor Email Sending
```bash
# Check Gmail API quota
python -c "from google.auth.transport.requests import Request; from google.oauth2.credentials import Credentials; creds = Credentials.from_authorized_user_file('token.json'); print(creds)"

# Verify emails in database
sqlite3 data/leads.db "SELECT email, status, sent_at FROM emails LIMIT 10"
```

---

## Step 5: Troubleshooting

### Scraper Blocked by Instagram
**Problem:** Instagram blocks requests after 100-200 posts
**Solution:**
1. Increase delays in .env: `SCROLL_DELAY=5-10`
2. Use residential proxy (Bright Data, Smartproxy)
3. Scrape during different hours
4. Split across multiple accounts

### Low Email Deliverability
**Problem:** Emails going to spam
**Solution:**
1. Warm up gradually (50 → 100 → 200 → 500/day over 2 weeks)
2. Setup domain authentication (SPF, DKIM, DMARC)
3. Improve email template (less salesy, more personalized)
4. Monitor bounce rates, remove invalid emails

### Cloud Instance Crashes
**Problem:** Out of memory (especially Google e2-micro)
**Solution:**
1. Make sure swap file is created (see Step 3)
2. Limit scraper to 100 posts per session
3. Upgrade to e2-small instance ($10/month)
4. Use Railway/Render instead (more memory)

### Gmail API Quota Exceeded
**Problem:** "Daily quota exceeded" error
**Solution:**
1. Free Gmail: Max 100 emails/day
2. Upgrade to Google Workspace: 1,500 emails/day
3. Switch to alternative service (Sendgrid, Brevo)

---

## Step 6: Maintenance & Optimization

### Daily Checks
```bash
# Every morning, check:
tail -50 logs/automation_manager.log  # Recent errors
sqlite3 data/leads.db "SELECT COUNT(*) FROM emails WHERE status='pending'"  # Pending emails
```

### Weekly Tasks
1. **Monitor bounce rates** - Remove invalid emails
2. **Check response rate** - Adjust template if <1%
3. **Review logs** - Look for patterns in failures
4. **Verify database size** - Should grow ~500 rows daily

### Monthly Optimization
1. **A/B test email templates** - Try different subject lines
2. **Clean database** - Remove duplicates/invalid emails
3. **Review scraping** - Check if new sources needed
4. **Analyze responses** - What's working, what's not

---

## Expected Results

### Daily Output
- **Posts scraped:** 500 unique Instagram posts
- **Emails extracted:** 200-300 per 500 posts (40-60% extraction rate)
- **Emails sent:** 500 (will queue and send remaining next day)
- **Database size:** +500 rows daily
- **Storage needed:** ~1MB data per day (100GB/year)

### Monthly Projection
- **Posts:** 15,000 new posts
- **Emails collected:** 6,000-9,000
- **Emails sent:** 15,000 (3x/month cap due to scraper limits)
- **Response rate:** 2-5% = 300-750 responses
- **Qualified leads:** 100-250 actual prospects

### Annual Projection
- **Posts collected:** 180,000
- **Emails:** 72,000-108,000
- **Campaigns sent:** ~50,000 emails
- **Responses:** 1,000-2,500
- **Qualified leads:** 500-1,500

---

## Cost Breakdown (Monthly)

| Item | Cost | Notes |
|------|------|-------|
| **Google Cloud e2-micro** | $0 | Free tier (1GB RAM) |
| **Claude API** | $10-30 | OCR text extraction |
| **Gmail API** | $0 | Free (100/day) or $6 Google Workspace (1500/day) |
| **Storage** | $0-5 | <100GB included |
| **Total** | $10-36 | Fully automated |

**OR Use Railway/Render:**
| Item | Cost |
|------|------|
| Railway | $5-15/month |
| Claude API | $10-30 |
| Gmail/Workspace | $0-6 |
| **Total** | $15-51 |

---

## Advanced: Custom Schedules

Edit `automation_manager.py` to customize timing:

```python
# Daily at specific UTC times:
schedule.every().day.at("02:00").do(self.run_scraper)       # 2 AM UTC
schedule.every().day.at("04:00").do(self.run_ocr)           # 4 AM UTC
schedule.every().day.at("09:00").do(self.run_full_pipeline) # 9 AM UTC

# Or run specific phases:
schedule.every().day.at("14:00").do(self.run_email_campaign) # 2 PM UTC
```

Convert UTC to your timezone:
- **UTC-5 (EST):** 02:00 UTC = 9 PM previous day
- **UTC+0 (GMT):** 02:00 UTC = 2 AM
- **UTC+8 (HK/SG):** 02:00 UTC = 10 AM
- **UTC+5:30 (IST):** 02:00 UTC = 7:30 AM

---

## Monitoring & Alerts

### Add Email Alerts (Optional)
```python
# In automation_manager.py, add after errors:
def send_alert_email(self, subject, message):
    import smtplib
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(os.getenv('FROM_EMAIL'), os.getenv('GMAIL_APP_PASSWORD'))
        smtp.send_message(f"Subject: {subject}\n\n{message}")
```

### Slack Notifications (Optional)
```python
def send_slack_alert(self, message):
    import requests
    webhook_url = os.getenv('SLACK_WEBHOOK_URL')
    requests.post(webhook_url, json={"text": message})
```

---

## Next Steps

1. **Deploy now:** Choose cloud provider and deploy
2. **Test manually:** Run `python automation_manager.py` locally first
3. **Monitor first week:** Check logs daily
4. **Optimize based on results:** Adjust timing/limits as needed
5. **Scale up:** If working well, increase POST/EMAIL targets

---

## Support & Debugging

**Check logs:**
```bash
tail -100 logs/automation_manager.log
```

**Test individual phases:**
```bash
python 1_scraper/instagram_scraper_pro.py
python 2_ocr/process_images_pro.py
python 3_email_extractor/extract_emails_pro.py
python 4_email_sender/send_campaign_pro.py --live
```

**Database queries:**
```bash
sqlite3 data/leads.db "SELECT * FROM emails LIMIT 5"
sqlite3 data/leads.db "SELECT status, COUNT(*) FROM emails GROUP BY status"
```

---

**Ready to deploy? Start with Google Cloud free tier and scale from there! 🚀**
