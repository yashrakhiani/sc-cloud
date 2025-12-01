# 📋 Quick Reference Guide

**Common commands and troubleshooting for StructCrew Lead Gen**

---

## 🚀 Setup (First Time)

```bash
# Automated setup
python setup.py

# Manual setup
pip install -r requirements.txt
playwright install chromium
python -m spacy download en_core_web_sm
copy .env.template .env
```

---

## 📸 Phase 1: Scraping

### Run Scraper
```bash
python 1_scraper/instagram_scraper_pro.py
```

### Configure
Edit `.env`:
```env
MAX_POSTS=500          # Number of posts to download
HEADLESS=false         # Set true for background mode
```

### Troubleshooting
```bash
# If Instagram blocks you:
# 1. Increase delays in .env
SCROLL_DELAY_MIN=5
SCROLL_DELAY_MAX=10

# 2. Use VPN/proxy
# 3. Scrape during off-peak hours
# 4. Reduce MAX_POSTS to 100-200
```

---

## 🔍 Phase 2: OCR

### Run OCR
```bash
python 2_ocr/process_images_pro.py
```

### Switch to Tesseract (Free)
Edit `.env`:
```env
USE_CLAUDE=false
```

### Check Results
```bash
# View extracted text
type data\extracted_text\post_00001.txt

# Check stats
type data\extracted_text\processing_stats.json
```

---

## 📧 Phase 3: Email Extraction

### Extract Emails
```bash
python 3_email_extractor/extract_emails_pro.py
```

### Query Database
```bash
# Check total leads
sqlite3 data/leads.db "SELECT COUNT(*) FROM leads"

# View sample
sqlite3 data/leads.db "SELECT * FROM leads LIMIT 10"

# Check by status
sqlite3 data/leads.db "SELECT status, COUNT(*) FROM leads GROUP BY status"

# Export to CSV
sqlite3 data/leads.db ".mode csv" ".headers on" ".output leads.csv" "SELECT * FROM leads"
```

---

## ✉️ Phase 4A: Send Emails (Gmail API)

### Setup Gmail API
1. Visit https://console.cloud.google.com/
2. Create project: "StructCrew-LeadGen"
3. Enable Gmail API
4. Create OAuth credentials (Desktop app)
5. Download as `credentials.json`
6. Run script (browser will open for auth)

### Send Campaign
```bash
python 4_email_sender/send_campaign_pro.py
```

### Monitor
```bash
# Check logs
type logs\email_campaign.log

# Check sent count
sqlite3 data/leads.db "SELECT COUNT(*) FROM leads WHERE status='sent'"

# Check remaining
sqlite3 data/leads.db "SELECT COUNT(*) FROM leads WHERE status='new'"
```

---

## ✉️ Phase 4B: Send Emails (Google Apps Script)

### Setup (One-time)
1. Create Google Sheet: "StructCrew Leads"
2. Add columns: `Company | Email | Status | Sent_At`
3. Export leads:
   ```bash
   sqlite3 data/leads.db ".mode csv" ".headers on" ".output leads.csv" "SELECT company, email FROM leads WHERE status='new'"
   ```
4. Import `leads.csv` to Google Sheet
5. Tools > Script Editor
6. Copy code from `4_email_sender/GoogleAppsScript.gs`
7. Save and authorize

### Run Campaign
In Google Sheet:
- Menu: **📧 Email Campaign > Send Batch Emails**

### Automate
In Google Sheet:
- Menu: **📧 Email Campaign > Setup Daily Trigger**

---

## 🛠️ Maintenance Commands

### Check Logs
```bash
type logs\scraper.log
type logs\ocr.log
type logs\email_extraction.log
type logs\email_campaign.log
```

### Clear Logs
```bash
del logs\*.log
```

### Reset Database Status
```sql
-- Reset all to 'new'
sqlite3 data/leads.db "UPDATE leads SET status='new', sent_at=NULL"

-- Reset failed only
sqlite3 data/leads.db "UPDATE leads SET status='new' WHERE status='failed'"
```

### Backup Database
```bash
copy data\leads.db data\leads_backup_%date:~-4,4%%date:~-10,2%%date:~-7,2%.db
```

### Export Specific Leads
```bash
# By domain
sqlite3 data/leads.db ".mode csv" ".output gmail_leads.csv" "SELECT * FROM leads WHERE email LIKE '%@gmail.com'"

# By company
sqlite3 data/leads.db ".mode csv" ".output studio_leads.csv" "SELECT * FROM leads WHERE company LIKE '%studio%'"
```

---

## 📊 Analytics Queries

### Lead Stats
```sql
-- Total leads
SELECT COUNT(*) FROM leads;

-- By status
SELECT status, COUNT(*) FROM leads GROUP BY status;

-- Top domains
SELECT SUBSTR(email, INSTR(email, '@')+1) as domain, COUNT(*) as count 
FROM leads 
GROUP BY domain 
ORDER BY count DESC 
LIMIT 10;

-- Leads with companies identified
SELECT COUNT(*) FROM leads WHERE company != 'Unknown';

-- Recent sends
SELECT company, email, sent_at 
FROM leads 
WHERE status='sent' 
ORDER BY sent_at DESC 
LIMIT 20;
```

### Email Stats
```sql
-- Success rate
SELECT 
  status,
  COUNT(*) as count,
  ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM leads), 2) as percentage
FROM leads
GROUP BY status;

-- Sends per day
SELECT 
  DATE(sent_at) as date,
  COUNT(*) as emails_sent
FROM leads
WHERE status='sent'
GROUP BY DATE(sent_at)
ORDER BY date DESC;
```

---

## 🔧 Troubleshooting

### Scraper Issues
```bash
# Instagram login loop
# → Delete cookies file and log in manually
del data\instagram_cookies.json

# Slow scraping
# → Run in headless mode
# Edit .env: HEADLESS=true

# Not enough posts downloaded
# → Check MAX_POSTS in .env
# → Instagram may have fewer posts than expected
```

### OCR Issues
```bash
# Claude API errors
# → Check API key in .env
# → Check quota at https://console.anthropic.com/
# → Switch to Tesseract: USE_CLAUDE=false

# Poor text quality
# → Use Claude instead of Tesseract
# → Images may be low quality (check raw_images/)
```

### Email Sending Issues
```bash
# Gmail quota exceeded
# → Wait until midnight PST (quota resets)
# → Check: sqlite3 data/leads.db "SELECT sent_at FROM leads WHERE status='sent' ORDER BY sent_at DESC LIMIT 1"

# Authentication failed
# → Delete token.json and re-authenticate
del data\token.json

# Bounces/spam complaints
# → Stop sending immediately
# → Review COMPLIANCE_CHECKLIST.md
# → Clean your list
# → Improve email content
```

---

## ⚡ Performance Tips

### Speed Up Scraping
```env
# Use headless mode
HEADLESS=true

# Reduce delays (risky - may trigger ban)
SCROLL_DELAY_MIN=2
SCROLL_DELAY_MAX=4
```

### Speed Up OCR
```env
# Use Tesseract (faster but less accurate)
USE_CLAUDE=false

# OR process in batches
OCR_BATCH_SIZE=100
```

### Speed Up Email Sending
```bash
# Use Google Apps Script (15x faster)
# 1,500 emails/day vs 100/day with Gmail API
```

---

## 🔐 Security

### Protect Credentials
```bash
# Never commit these files to Git:
.env
credentials.json
data/token.json
data/instagram_cookies.json

# Check .gitignore
type .gitignore
```

### Secure Database
```bash
# Encrypt database (optional)
# Use tools like SQLCipher for production
```

---

## 📞 Support

### Get Help
1. Check logs first: `type logs\*.log`
2. Review README.md
3. Check COMPLIANCE_CHECKLIST.md
4. Review workflow: `.agent/workflows/lead-gen-pipeline.md`

### Report Issues
Include:
- Error message from logs
- Steps to reproduce
- Python version: `python --version`
- Installed packages: `pip freeze`

---

## ✅ Pre-Flight Checklist

Before running full campaign:

- [ ] Tested scraper with 10 posts
- [ ] Tested OCR on sample images
- [ ] Database has at least 50 leads
- [ ] Email template customized
- [ ] Compliance checklist completed
- [ ] Test email sent to yourself
- [ ] Unsubscribe mechanism tested
- [ ] Business address added to email
- [ ] Daily monitoring plan in place

---

**Quick Start:** `python setup.py` → Edit `.env` → Run workflow

**Emergency Stop:** Delete `data/token.json` to prevent further Gmail sends
