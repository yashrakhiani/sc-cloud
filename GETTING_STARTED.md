# 🚀 Getting Started - StructCrew Lead Gen

**Your complete guide to running your first campaign tomorrow**

---

## ⏰ Time Required

- **Setup:** 30-60 minutes
- **Test run:** 1-2 hours
- **Full campaign:** 7-14 days (automated)

---

## 📋 Step-by-Step Guide

### ✅ Step 1: Automated Setup (15 minutes)

Open terminal in project folder and run:

```bash
python setup.py
```

This will:
- ✓ Check Python version (need 3.11+)
- ✓ Create necessary directories
- ✓ Install Python packages
- ✓ Install Playwright browsers
- ✓ Install spaCy language model
- ✓ Create `.env` file from template

**If setup fails:** See [Manual Setup](#manual-setup-alternative) below

---

### ✅ Step 2: Get API Keys (15 minutes)

#### A. Claude API Key (For OCR)

1. Visit https://console.anthropic.com/
2. Sign up / Log in
3. Navigate to **API Keys**
4. Click **Create Key**
5. Copy the key (starts with `sk-ant-...`)

💰 **Cost:** ~$0.003/image (~$60 for 20,000 images)

#### B. Gmail API Credentials (For Email Sending)

1. Visit https://console.cloud.google.com/
2. Create new project: "StructCrew-LeadGen"
3. Enable **Gmail API**:
   - Click "Enable APIs and Services"
   - Search "Gmail API"
   - Click "Enable"
4. Create **OAuth 2.0 Credentials**:
   - Go to "Credentials" tab
   - Click "Create Credentials" > "OAuth client ID"
   - Application type: **Desktop app**
   - Name: "StructCrew Sender"
   - Click "Create"
5. **Download** credentials:
   - Click download icon (⬇️) next to your new credentials
   - Save as `credentials.json` in project root folder

⏱️ **First run:** Browser will open for authentication (one-time)

---

### ✅ Step 3: Configure Environment (5 minutes)

Open `.env` file in text editor and fill in:

```env
# REQUIRED
CLAUDE_API_KEY=sk-ant-xxxxxxxxxxxxx    # From Step 2A
FROM_NAME=Your Name                     # Your actual name
FROM_EMAIL=your.email@gmail.com         # Your Gmail address

# OPTIONAL (recommended to customize)
MAX_POSTS=500                           # Start with 500, increase later
SUBJECT=Architecture Collaboration Opportunity
DAILY_EMAIL_LIMIT=100                   # 100 for Gmail, 1500 for Workspace
```

**Save the file** when done.

---

### ✅ Step 4: Customize Email Template (10 minutes)

Edit `templates/cold_email.html`:

1. Replace **"Your Name"** with your actual name
2. Replace **"yoursite.com"** with your website
3. Add your **business address** (legally required):
   ```html
   [Your Business Name]<br>
   [Street Address]<br>
   [City, State, ZIP]
   ```
4. Update **Calendly link** or remove if not using:
   ```html
   <a href="https://calendly.com/your-link" class="cta-button">
   ```
5. Customize **value proposition** to match your services

**Save the file** when done.

---

### ✅ Step 5: Test Run (30 minutes)

#### Test 1: Scraper (Download 10 posts)

Edit `.env` and set:
```env
MAX_POSTS=10
HEADLESS=false
```

Run:
```bash
python 1_scraper/instagram_scraper_pro.py
```

**What to expect:**
- Browser opens to Instagram
- If not logged in: **Log in manually** (cookies will be saved)
- Scraper downloads 10 images to `data/raw_images/`
- Progress bar shows download status

**Troubleshooting:**
- If login fails: Delete `data/instagram_cookies.json` and try again
- If scraping is slow: Normal, it's using human-like delays to avoid bans

---

#### Test 2: OCR (Extract text from 10 images)

Run:
```bash
python 2_ocr/process_images_pro.py
```

**What to expect:**
- Processes 10 images (takes 1-2 minutes)
- Uses Claude Vision API
- Saves extracted text to `data/extracted_text/`
- Shows progress bar

**Check results:**
```bash
type data\extracted_text\post_00001.txt
```

**Troubleshooting:**
- If Claude API fails: Check API key in `.env`
- If quota exceeded: Switch to Tesseract (set `USE_CLAUDE=false` in `.env`)

---

#### Test 3: Email Extraction (Build database)

Run:
```bash
python 3_email_extractor/extract_emails_pro.py
```

**What to expect:**
- Processes all text files
- Extracts emails, companies, phones
- Creates SQLite database: `data/leads.db`
- Exports CSV: `data/leads_export.csv`

**Check results:**
```bash
sqlite3 data/leads.db "SELECT * FROM leads"
```

**Expected:** 4-6 emails extracted from 10 posts (40-60% hit rate)

---

#### Test 4: Send Email (To yourself ONLY)

**IMPORTANT:** First, send to yourself to test template!

Edit `4_email_sender/send_campaign_pro.py` temporarily:

Find this line (around line 330):
```python
cursor.execute('''
    SELECT * FROM leads
    WHERE status = 'new' AND is_valid_email = 1
    ORDER BY id
    LIMIT ?
''', (limit,))
```

Replace with:
```python
# TEST: Send to yourself only
cursor.execute('''
    SELECT * FROM leads
    WHERE email = 'your.email@gmail.com'
    LIMIT 1
''', ())
```

Run:
```bash
python 4_email_sender/send_campaign_pro.py
```

**What to expect:**
- Browser opens for Gmail authentication (first time only)
- Sends 1 email to yourself
- Check your inbox!

**Check the email:**
- ✅ Renders correctly (desktop + mobile)
- ✅ All links work
- ✅ Personalization variables filled in
- ✅ Unsubscribe link present
- ✅ Business address shown

**If email looks good:** You're ready! Undo the test change above.

---

### ✅ Step 6: Review Compliance (10 minutes)

**CRITICAL:** Read this before sending to real leads!

Open `COMPLIANCE_CHECKLIST.md` and complete:

- [ ] Business address in email
- [ ] Unsubscribe mechanism tested
- [ ] Subject line not misleading
- [ ] From name is accurate
- [ ] Ready to process opt-outs within 10 days

**Legal warning:** Sending spam can result in fines up to $50,120 per email (CAN-SPAM).

---

### ✅ Step 7: Pilot Campaign (Start small!)

**Don't go big yet!** Start with 50-100 leads to validate everything works.

Edit `.env`:
```env
MAX_POSTS=100              # Scrape 100 posts (expect ~40-60 emails)
DAILY_EMAIL_LIMIT=50       # Send to 50 leads max
```

Run complete pipeline:
```bash
# Download 100 posts
python 1_scraper/instagram_scraper_pro.py

# Extract text
python 2_ocr/process_images_pro.py

# Build database
python 3_email_extractor/extract_emails_pro.py

# Send emails (to real leads now)
python 4_email_sender/send_campaign_pro.py
```

**Monitor for 48 hours:**
- Check bounce rate: Should be <5%
- Check spam complaints: Should be 0%
- Check responses: Expect 1-3 replies from 50 sends
- Check logs: `type logs\email_campaign.log`

**If metrics look good:** Scale up!

---

### ✅ Step 8: Scale to Full Campaign

Edit `.env`:
```env
MAX_POSTS=20000            # Full scrape
DAILY_EMAIL_LIMIT=100      # Gmail limit (or 1500 for Workspace)
```

Run pipeline again:
```bash
python 1_scraper/instagram_scraper_pro.py    # Takes 10-20 hours
python 2_ocr/process_images_pro.py           # Takes 5-10 hours
python 3_email_extractor/extract_emails_pro.py  # Takes 1-2 hours
```

**Expected database:** 8,000-12,000 leads

Send daily:
```bash
# Run this once per day
python 4_email_sender/send_campaign_pro.py
```

**Timeline:**
- Gmail API (100/day): ~80-120 days for 10k leads
- Google Workspace (1,500/day): ~7 days for 10k leads

---

## 🔄 Daily Workflow (5 minutes/day)

Once campaign is running:

```bash
# 1. Send daily batch
python 4_email_sender/send_campaign_pro.py

# 2. Check logs
type logs\email_campaign.log

# 3. Check responses
# Check your Gmail inbox for replies

# 4. Process unsubscribes
# If someone replies "UNSUBSCRIBE", update database:
sqlite3 data/leads.db "UPDATE leads SET status='unsubscribed' WHERE email='their@email.com'"
```

---

## 🚀 Faster Option: Google Apps Script (1,500/day)

If you have **Google Workspace** ($6/month), use Apps Script for 15x speed:

1. Create Google Sheet: "StructCrew Leads"
2. Export database:
   ```bash
   sqlite3 data/leads.db ".mode csv" ".headers on" ".output leads.csv" "SELECT company, email FROM leads WHERE status='new'"
   ```
3. Import `leads.csv` to Google Sheet
4. Tools > Script Editor
5. Copy code from `4_email_sender/GoogleAppsScript.gs`
6. Save and run: **📧 Email Campaign > Send Batch Emails**

**Automate:**  
Menu > **Setup Daily Trigger** (runs at 9 AM daily automatically)

---

## 📊 Expected Results

From 20,000 Instagram posts:

| Metric | Expected | Actual (Track Here) |
|--------|----------|---------------------|
| Posts downloaded | 17,000-19,000 | ___ |
| Text extracted | 16,000-18,000 | ___ |
| Emails found | 8,000-12,000 | ___ |
| Emails sent | 8,000-12,000 | ___ |
| Emails delivered | 6,400-11,400 (80-95%) | ___ |
| Emails opened | 1,600-3,420 (20-30%) | ___ |
| Responses | 160-600 (2-5%) | ___ |
| Qualified leads | 80-300 (1-2.5%) | ___ |

---

## ❓ FAQs

### Q: Do I need Google Workspace?
**A:** No. Free Gmail works (100/day). Workspace is optional for higher volume (1,500/day).

### Q: What does Claude API cost?
**A:** ~$0.003/image. For 20k images = ~$60 total.

### Q: Can I use free OCR?
**A:** Yes! Set `USE_CLAUDE=false` in `.env` to use Tesseract (free, but 70-80% accuracy vs 95% with Claude).

### Q: Is Instagram scraping legal?
**A:** It violates Instagram's TOS. Use at your own risk. Consider official APIs or public data sources.

### Q: Will I avoid spam folder?
**A:** 80-95% inbox rate if you follow deliverability best practices (warm up, authenticate, personalize).

### Q: How do I avoid getting banned from Instagram?
**A:** Use human-like delays, don't scrape too fast, use VPN, scrape during off-peak hours, limit to 100-200 posts/session.

### Q: What if Gmail blocks me?
**A:** Happens if you send too fast or get spam complaints. Wait 24 hours, reduce volume, improve email quality.

---

## 🆘 Troubleshooting

### Issue: Instagram login fails
```bash
# Delete cookies and try again
del data\instagram_cookies.json
python 1_scraper/instagram_scraper_pro.py
```

### Issue: Claude API error
```bash
# Check API key
notepad .env
# OR switch to Tesseract
# Edit .env: USE_CLAUDE=false
```

### Issue: No emails extracted
```bash
# Check OCR quality
type data\extracted_text\post_00001.txt
# If text is garbled, use Claude instead of Tesseract
```

### Issue: Gmail authentication fails
```bash
# Delete token and re-authenticate
del data\token.json
python 4_email_sender/send_campaign_pro.py
```

---

## 📚 Next Steps After Reading This

1. ✅ Run `python setup.py`
2. ✅ Get Claude API key
3. ✅ Get Gmail credentials
4. ✅ Edit `.env` file
5. ✅ Customize email template
6. ✅ Run test with 10 posts
7. ✅ Send test email to yourself
8. ✅ Read compliance checklist
9. ✅ Run pilot with 50 leads
10. ✅ Scale up if metrics are good

---

## 🎉 You're Ready!

Everything is prepared. Just follow the steps above and you'll have:
- ✅ Thousands of qualified leads
- ✅ Automated email campaigns
- ✅ Professional outreach system
- ✅ Compliance safeguards

**Start with Step 1 tomorrow morning. Good luck! 🚀**

---

**Questions?** Check:
- `README.md` - Full documentation
- `QUICK_REFERENCE.md` - Common commands
- `COMPLIANCE_CHECKLIST.md` - Legal requirements
- `logs/` - Error logs

**Emergency stop:** Delete `data/token.json` to prevent further Gmail sends
