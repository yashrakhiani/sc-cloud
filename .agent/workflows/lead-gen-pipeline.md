---
description: Complete lead generation pipeline setup and execution
---

# StructCrew Lead Generation Pipeline - Complete Workflow

## Phase 0: Environment Setup (First Time Only)

### Step 1: Install Python Dependencies
```bash
pip install -r requirements.txt
```

// turbo
### Step 2: Install Playwright Browsers
```bash
playwright install chromium
```

### Step 3: Install spaCy Language Model
```bash
python -m spacy download en_core_web_sm
```

### Step 4: Configure Environment Variables
1. Copy `.env.template` to `.env`
2. Fill in your credentials:
   - `CLAUDE_API_KEY` - Get from https://console.anthropic.com/
   - `FROM_NAME` - Your name for email sending
   - `FROM_EMAIL` - Your Gmail address
   - Update other settings as needed

### Step 5: Set up Gmail API (For Python Email Sender)
1. Go to https://console.cloud.google.com/
2. Create new project: "StructCrew-LeadGen"
3. Enable Gmail API
4. Create OAuth 2.0 credentials (Desktop app)
5. Download as `credentials.json` in project root
6. First run will open browser for authentication

---

## Phase 1: Scrape Instagram Posts

// turbo
### Test Scraper (10 posts)
```bash
python 1_scraper/instagram_scraper_pro.py
```

**Manual Steps:**
- Browser will open (not headless mode by default)
- Log in to Instagram manually if needed
- Wait for scraper to download images
- Cookies will be saved for future runs

**Output:** Images saved to `data/raw_images/`

### Production Run (Customize in .env)
Edit `.env` and set `MAX_POSTS=500` (or higher), then run scraper again.

---

## Phase 2: OCR Text Extraction

// turbo
### Run OCR Processing
```bash
python 2_ocr/process_images_pro.py
```

**What it does:**
- Processes all images in `data/raw_images/`
- Uses Claude Vision API (or Tesseract fallback)
- Extracts structured text
- Saves to `data/extracted_text/`

**Cost Estimate:** ~$0.003/image with Claude Haiku

---

## Phase 3: Extract Emails & Build Database

// turbo
### Run Email Extraction
```bash
python 3_email_extractor/extract_emails_pro.py
```

**What it does:**
- Parses all text files
- Extracts emails, company names, phones, websites
- Validates emails
- Stores in SQLite database: `data/leads.db`
- Exports to CSV: `data/leads_export.csv`

**Output:** SQLite database with all leads

---

## Phase 4A: Send Emails (Gmail API - 100/day)

### Test with Single Email
Edit `4_email_sender/send_campaign_pro.py` and test with limit=1

// turbo
### Run Campaign
```bash
python 4_email_sender/send_campaign_pro.py
```

**What it does:**
- Reads leads from database (status='new')
- Personalizes email template
- Sends via Gmail API
- Updates database with sent status
- Respects daily limits (100 for free Gmail)

**Daily Schedule:** Run this script once per day until all leads contacted

---

## Phase 4B: Send Emails (Google Apps Script - 1,500/day)

### Setup Google Apps Script (One-time)
1. Create new Google Sheet: "StructCrew Leads"
2. Add columns: `Company | Email | Status | Sent_At`
3. Export your leads: 
   ```bash
   sqlite3 data/leads.db ".mode csv" ".headers on" ".output leads.csv" "SELECT company, email FROM leads WHERE status='new'"
   ```
4. Import `leads.csv` to Google Sheet
5. In Sheet: **Tools > Script Editor**
6. Copy/paste code from `4_email_sender/GoogleAppsScript.gs`
7. Save and run `onOpen()` function
8. Authorize permissions
9. Use menu: **📧 Email Campaign > Send Batch Emails**

### Automate (Optional)
- In Script Editor: **📧 Email Campaign > Setup Daily Trigger**
- Will run automatically at 9 AM daily

---

## Monitoring & Maintenance

### Check Database Stats
```bash
sqlite3 data/leads.db "SELECT status, COUNT(*) FROM leads GROUP BY status"
```

### View Logs
```bash
type logs\scraper.log
type logs\ocr.log
type logs\email_extraction.log
type logs\email_campaign.log
```

### Export Leads to CSV
Database is auto-exported, but you can manually run:
```bash
python 3_email_extractor/extract_emails_pro.py
```

---

## Compliance & Best Practices

### Before Sending Emails:
1. ✅ Update email template with your real information
2. ✅ Add your business address (legally required)
3. ✅ Test template on yourself first
4. ✅ Set up unsubscribe email inbox
5. ✅ Monitor spam complaints
6. ✅ Respect unsubscribe requests immediately

### Deliverability Optimization:
1. **Warm up your domain:** Start with 50 emails/day, increase gradually
2. **Personalization is key:** Customize company names, mention specific job posts
3. **Monitor metrics:** Track opens, clicks, bounces, spam complaints
4. **Clean your list:** Remove bounced emails immediately
5. **Authenticate your domain:** Set up SPF, DKIM, DMARC records

### Legal Requirements:
- **CAN-SPAM (US):** Include physical address, clear unsubscribe, accurate subject
- **GDPR (EU):** Only contact if you have legitimate interest, honor opt-outs within 30 days
- **CASL (Canada):** Need consent or existing business relationship

---

## Troubleshooting

### Instagram blocks you:
- Increase delays in scraper: `SCROLL_DELAY = (5, 10)`
- Use VPN or proxy
- Scrape during off-peak hours (night time PST)
- Limit to 100-200 posts per session

### Claude API rate limits:
- Add longer delays: `RATE_LIMIT_DELAY = 2`
- Process in smaller batches
- Switch to Tesseract: Set `USE_CLAUDE=false` in `.env`

### Gmail sending fails:
- Check quota: Run script again tomorrow
- Enable "Less secure app access" (if using app password)
- Use Gmail API instead of SMTP
- Upgrade to Google Workspace for higher limits

### Low email extraction rate:
- Review OCR quality in `data/extracted_text/`
- Adjust Claude prompt in `process_images_pro.py`
- Some posts may not have emails (expected)

---

## Expected Timeline & Results

### Timeline:
- **Setup:** 1-2 hours
- **Scraping 20k posts:** 10-20 hours (automated)
- **OCR processing:** 5-10 hours (automated)
- **Email extraction:** 1-2 hours (automated)
- **Sending 10k emails:** 
  - Gmail API (100/day): ~100 days
  - Google Workspace (1,500/day): ~7 days

### Expected Results:
- **Scraping success:** 85-95% of posts downloaded
- **Email extraction rate:** 40-60% (8k-12k emails from 20k posts)
- **Email deliverability:** 80-95% inbox placement
- **Response rate:** 2-5% (industry standard for cold emails)
- **Qualified leads:** 160-600 interested studios

---

## Next Steps After First Campaign

1. **Analyze results:** Track opens, clicks, responses
2. **A/B test templates:** Try different subject lines, CTAs
3. **Follow up:** Send 2-3 follow-up emails to non-responders (spaced 1 week apart)
4. **Expand sources:** Scrape other Instagram accounts, LinkedIn, job boards
5. **Build CRM:** Integrate with Airtable, HubSpot, or similar
6. **Automate responses:** Use Zapier for auto-reply detection

---

**Ready to generate leads! 🚀**
