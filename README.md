# 🎯 StructCrew Lead Generation System

**Automated lead generation pipeline** to extract studio contact information from Instagram job postings and send targeted outreach emails.

> **Status:** Production-Ready  
> **Last Updated:** November 27, 2025  
> **Version:** 2.0 (Playwright + Claude Vision + Google Apps Script)

---

## 📊 Quick Stats

- **Target Source:** [@archijobs](https://instagram.com/archijobs) (20,000+ architecture job posts)
- **Expected Leads:** 8,000-12,000 unique emails
- **Email Capacity:** Up to 1,500 emails/day (Google Workspace)
- **Response Rate:** 2-5% industry standard
- **Timeline:** 7-14 days for full campaign

---

## 🚀 Features

### Phase 1: Instagram Scraper
- ✅ **Playwright-based** (faster & more reliable than Selenium)
- ✅ Anti-ban protections (random delays, human-like behavior)
- ✅ Cookie persistence (stay logged in)
- ✅ Metadata tracking (post URLs, alt text, timestamps)
- ✅ Configurable limits & filters

### Phase 2: OCR Text Extraction
- ✅ **Claude Vision API** (superior accuracy for job posts)
- ✅ Tesseract fallback (free alternative)
- ✅ Structured data extraction (company, email, phone, job title)
- ✅ Batch processing with rate limiting
- ✅ Error recovery & resumability

### Phase 3: Email Extraction & Database
- ✅ **NLP-powered** company name extraction (spaCy)
- ✅ Email validation (syntax + basic deliverability checks)
- ✅ **SQLite database** with full-text search
- ✅ Deduplication & data quality tracking
- ✅ CSV export for external tools

### Phase 4: Email Campaign
- ✅ **Gmail API** (100 emails/day - free tier)
- ✅ **Google Apps Script** (1,500 emails/day - Workspace)
- ✅ Beautiful HTML email templates (mobile-responsive)
- ✅ Personalization (company name, job details)
- ✅ Compliance features (unsubscribe, CAN-SPAM/GDPR)
- ✅ Deliverability optimization (delays, headers, auth)

---

## 📁 Project Structure

```
StructCrew_LeadGen/
├── 1_scraper/
│   ├── instagram_scraper_pro.py    # Playwright scraper (PRODUCTION)
│   └── instagram_scraper.py        # Legacy Selenium version
│
├── 2_ocr/
│   ├── process_images_pro.py       # Claude Vision + Tesseract (PRODUCTION)
│   └── process_images.py           # Legacy version
│
├── 3_email_extractor/
│   ├── extract_emails_pro.py       # NLP + SQLite extractor (PRODUCTION)
│   └── extract_emails.py           # Legacy version
│
├── 4_email_sender/
│   ├── send_campaign_pro.py        # Gmail API sender (PRODUCTION)
│   ├── GoogleAppsScript.gs         # Google Workspace (1500/day)
│   └── send_campaign.py            # Legacy version
│
├── data/
│   ├── raw_images/                 # Downloaded Instagram posts
│   ├── extracted_text/             # OCR results
│   ├── leads.db                    # SQLite database
│   ├── leads_export.csv            # CSV export
│   └── instagram_cookies.json      # Saved login session
│
├── templates/
│   └── cold_email.html             # Email template (customizable)
│
├── logs/                           # Processing logs
├── .agent/workflows/
│   └── lead-gen-pipeline.md        # Complete workflow guide
│
├── requirements.txt                # Python dependencies
├── .env.template                   # Configuration template
└── README.md                       # This file
```

---

## ⚡ Quick Start

### 1. Install Dependencies
```bash
# Install Python packages
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium

# Install spaCy language model
python -m spacy download en_core_web_sm
```

### 2. Configure Environment
```bash
# Copy template
copy .env.template .env

# Edit .env with your credentials
notepad .env
```

**Required credentials:**
- `CLAUDE_API_KEY` - Get from https://console.anthropic.com/
- `FROM_NAME` - Your name
- `FROM_EMAIL` - Your Gmail address

### 3. Run Pipeline
```bash
# Step 1: Scrape Instagram posts
python 1_scraper/instagram_scraper_pro.py

# Step 2: Extract text via OCR
python 2_ocr/process_images_pro.py

# Step 3: Build email database
python 3_email_extractor/extract_emails_pro.py

# Step 4: Send campaign (Gmail API)
python 4_email_sender/send_campaign_pro.py
```

**OR** use the workflow:
```bash
# See complete guide
cat .agent/workflows/lead-gen-pipeline.md
```

---

## 📧 Email Sending Options

### Option A: Gmail API (Free - 100 emails/day)
- ✅ Free forever
- ✅ Good for testing/small campaigns
- ⚠️ Limited to 100 emails/day
- **Setup:** 30 minutes (OAuth credentials)

### Option B: Google Apps Script (Workspace - 1,500/day)
- ✅ 15x higher limit (1,500/day)
- ✅ No server required (runs on Google Cloud)
- ✅ Beautiful HTML templates built-in
- ✅ Automated scheduling with triggers
- ⚠️ Requires Google Workspace (~$6/month)
- **Setup:** See `4_email_sender/GoogleAppsScript.gs`

### Option C: Alternatives
- **Brevo:** 300 emails/day (free)
- **Resend:** Unlimited (free, requires domain auth)
- **Mailtrap:** 1,000 emails/month (free tier)

---

## 🎨 Email Template Customization

Edit `templates/cold_email.html` to customize:
- **Brand colors** (currently purple gradient)
- **Your value proposition**
- **Call-to-action** (Calendly link, reply, etc.)
- **Company info** (address, phone, social links)

**Personalization variables:**
- `{company}` - Company name
- `{email}` - Recipient email
- `{job_title}` - Job posting title
- `{from_name}` - Your name
- `{unsubscribe_email}` - Unsubscribe email
- `{current_date}` - Current date

---

## 📊 Expected Results

### Scraping (Phase 1)
- **Success Rate:** 85-95%
- **Time:** 10-20 hours for 20k posts
- **Output:** ~18,000 images

### OCR (Phase 2)
- **Accuracy:** 90-95% with Claude Vision
- **Cost:** ~$60 for 20k images ($0.003/image)
- **Tesseract Alternative:** Free, 70-80% accuracy

### Email Extraction (Phase 3)
- **Extraction Rate:** 40-60% (not all posts have emails)
- **Expected Leads:** 8,000-12,000 unique emails
- **Company Identification:** 70-80% with NLP

### Email Campaign (Phase 4)
- **Deliverability:** 80-95% inbox placement
- **Open Rate:** 20-30% (industry avg for cold emails)
- **Response Rate:** 2-5%
- **Qualified Leads:** 160-600 interested studios

---

## ⚖️ Legal & Compliance

### ⚠️ Important Disclaimers

1. **Instagram Scraping:** Violates Instagram's Terms of Service. Use at your own risk.
2. **Email Laws:** Must comply with CAN-SPAM (US), GDPR (EU), CASL (Canada)
3. **Legitimate Interest:** Only contact businesses with relevant offers

### ✅ Compliance Features Built-in

- **Unsubscribe Links:** Every email has opt-out
- **Physical Address:** Template includes business address field
- **Clear Identification:** From name, company, purpose stated
- **Opt-out Tracking:** Database tracks email status
- **Privacy Policy:** Link to privacy policy (you must create)

### 🔒 Data Protection

- Email addresses stored locally in SQLite
- No data sent to third parties (except email providers)
- Secure credential storage (.env file - keep private!)
- Cookie files contain Instagram session (keep private!)

---

## 🛠️ Troubleshooting

### Instagram Blocks/Bans
```bash
# Solution 1: Increase delays
# Edit 1_scraper/instagram_scraper_pro.py
SCROLL_DELAY = (5, 10)  # Longer delays

# Solution 2: Use VPN/proxy
# Solution 3: Scrape during off-peak hours (night time PST)
# Solution 4: Limit to 100-200 posts per session
```

### Claude API Rate Limits
```bash
# Switch to Tesseract (free)
# Edit .env
USE_CLAUDE=false

# OR increase delays
# Edit 2_ocr/process_images_pro.py
RATE_LIMIT_DELAY = 2  # seconds
```

### Low Email Deliverability
1. **Warm up domain:** Start with 50 emails/day, increase gradually
2. **Authenticate:** Set up SPF, DKIM, DMARC records
3. **Personalize:** Customize templates heavily
4. **Monitor:** Check spam complaints, bounces
5. **Clean list:** Remove invalid/bounced emails

### Gmail Sending Fails
```bash
# Check quota
# Quota resets at midnight PST
# Free Gmail: 100/day
# Google Workspace: 1,500/day

# Enable Gmail API
# Visit: https://console.cloud.google.com/
# Make sure Gmail API is enabled
```

---

## 📈 Optimization Tips

### Deliverability (80% → 95%+)
1. **Domain Authentication:** SPF + DKIM + DMARC
2. **Warm-up Period:** 50 → 100 → 200 → 500/day over 2 weeks
3. **List Hygiene:** Validate emails, remove bounces
4. **Engagement:** Reply to responses quickly
5. **Content Quality:** Avoid spam words, use authentic language

### Response Rate (2% → 5%+)
1. **Hyper-Personalization:** Mention specific job post details
2. **Compelling Subject:** A/B test different angles
3. **Clear Value Prop:** What's in it for them?
4. **Social Proof:** Include testimonials, case studies
5. **Follow-up Sequence:** 2-3 follow-ups spaced 1 week apart

### Efficiency
1. **Batch Processing:** Process in increments (500 posts at a time)
2. **Resume Capability:** All scripts check for existing data
3. **Parallel Processing:** Run OCR overnight
4. **Database Queries:** Use SQLite for fast lookups

---

## 🔮 Future Enhancements

- [ ] **Multi-source scraping** (LinkedIn, job boards, company websites)
- [ ] **AI-powered personalization** (Claude-generated custom intros)
- [ ] **Email tracking** (open/click tracking with pixels)
- [ ] **CRM integration** (Airtable, HubSpot, Salesforce)
- [ ] **Auto-reply detection** (flag interested leads)
- [ ] **A/B testing framework** (test different templates)
- [ ] **Webhook notifications** (Slack/Discord alerts for responses)
- [ ] **Lead scoring** (prioritize high-value leads)

---

## 📚 Resources

### Documentation
- [Complete Workflow Guide](.agent/workflows/lead-gen-pipeline.md)
- [Gmail API Setup Guide](https://developers.google.com/gmail/api/quickstart/python)
- [Google Apps Script Docs](https://developers.google.com/apps-script)
- [Claude API Docs](https://docs.anthropic.com/claude/reference/getting-started-with-the-api)

### Tools
- [Mailtrap](https://mailtrap.io/) - Email testing
- [Mail Tester](https://www.mail-tester.com/) - Spam score checker
- [Hunter.io](https://hunter.io/) - Email verification
- [Calendly](https://calendly.com/) - Meeting scheduler

### Legal
- [CAN-SPAM Act](https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business)
- [GDPR Guidelines](https://gdpr.eu/)
- [CASL Compliance](https://crtc.gc.ca/eng/casl-lcap.htm)

---

## 🤝 Support

### Logs Location
```bash
logs/scraper.log           # Instagram scraping
logs/ocr.log               # Text extraction
logs/email_extraction.log  # Email database building
logs/email_campaign.log    # Email sending
```

### Database Queries
```bash
# Check lead stats
sqlite3 data/leads.db "SELECT status, COUNT(*) FROM leads GROUP BY status"

# Export specific companies
sqlite3 data/leads.db "SELECT * FROM leads WHERE company LIKE '%studio%'"

# Find emails with specific domain
sqlite3 data/leads.db "SELECT * FROM leads WHERE email LIKE '%@gmail.com'"
```

---

## 📝 License & Disclaimer

**Educational purposes only.** This tool is provided as-is for learning automation concepts.

- Instagram scraping may violate Terms of Service
- Use responsibly and respect privacy
- Comply with all applicable email marketing laws
- Author not liable for misuse

---

## ✨ Credits

**Created by:** StructCrew Development Team  
**AI Assistant:** Claude (Anthropic)  
**Version:** 2.0 Production-Ready  
**Date:** November 27, 2025

---

**Ready to generate leads? Run `/lead-gen-pipeline` to start! 🚀**
