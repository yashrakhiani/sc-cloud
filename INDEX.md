# 📑 StructCrew Lead Gen - Documentation Index

**Quick navigation to all project resources**

---

## 🚀 Start Here (Read in Order)

### 1. [GETTING_STARTED.md](GETTING_STARTED.md) ⭐
**Your complete step-by-step guide to running your first campaign**
- Setup instructions
- API key acquisition
- Test procedures
- Troubleshooting

### 2. [README.md](README.md)
**Complete project overview and documentation**
- Features & capabilities
- Architecture overview
- Expected results
- Setup guide

### 3. [COMPLIANCE_CHECKLIST.md](COMPLIANCE_CHECKLIST.md) ⚠️
**CRITICAL - Read before sending ANY emails**
- CAN-SPAM requirements (US)
- GDPR compliance (EU)
- CASL rules (Canada)
- Legal disclaimers

---

## 📖 Reference Documentation

### 4. [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
**Common commands and troubleshooting**
- Terminal commands
- SQL queries
- Configuration tips
- Performance optimization

### 5. [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
**High-level project overview**
- What's included
- Expected ROI
- Feature comparison
- Timeline

### 6. [.agent/workflows/lead-gen-pipeline.md](.agent/workflows/lead-gen-pipeline.md)
**Complete workflow guide with step-by-step instructions**
- Phase-by-phase breakdown
- Detailed commands
- Monitoring procedures
- Troubleshooting

---

## 🛠️ Technical Files

### Configuration

- **`.env.template`** - Configuration template (copy to `.env`)
- **`requirements.txt`** - Python dependencies
- **`.gitignore`** - Git ignore rules (protects credentials)

### Scripts

#### Phase 1: Scraping
- **`1_scraper/instagram_scraper_pro.py`** - Playwright-based scraper ⭐ (PRODUCTION)
- `1_scraper/instagram_scraper.py` - Legacy Selenium version

#### Phase 2: OCR
- **`2_ocr/process_images_pro.py`** - Claude Vision + Tesseract ⭐ (PRODUCTION)
- `2_ocr/process_images.py` - Legacy version

#### Phase 3: Email Extraction
- **`3_email_extractor/extract_emails_pro.py`** - NLP + SQLite ⭐ (PRODUCTION)
- `3_email_extractor/extract_emails.py` - Legacy version

#### Phase 4: Email Sending
- **`4_email_sender/send_campaign_pro.py`** - Gmail API sender ⭐ (PRODUCTION)
- **`4_email_sender/GoogleAppsScript.gs`** - Google Workspace (1500/day) ⭐
- `4_email_sender/send_campaign.py` - Legacy version

### Utilities
- **`setup.py`** - Automated setup script

### Templates
- **`templates/cold_email.html`** - Professional HTML email template
- `templates/default.txt` - Plain text fallback (legacy)

---

## 📂 Directory Structure

```
StructCrew_LeadGen/
├── 📄 Documentation (Start Here)
│   ├── GETTING_STARTED.md          ⭐ Read this first
│   ├── README.md                    Complete guide
│   ├── COMPLIANCE_CHECKLIST.md      ⚠️ Legal requirements
│   ├── QUICK_REFERENCE.md           Command reference
│   ├── PROJECT_SUMMARY.md           Overview
│   ├── INDEX.md                     This file
│   └── IMPLEMENTATION_PLAN.md       Original plan (legacy)
│
├── 🔧 Configuration
│   ├── .env.template                Config template
│   ├── .gitignore                   Git ignore rules
│   ├── requirements.txt             Python dependencies
│   └── setup.py                     Automated setup
│
├── 📸 Phase 1: Scraping
│   └── 1_scraper/
│       ├── instagram_scraper_pro.py ⭐ PRODUCTION
│       └── instagram_scraper.py     Legacy
│
├── 🔍 Phase 2: OCR
│   └── 2_ocr/
│       ├── process_images_pro.py    ⭐ PRODUCTION
│       └── process_images.py        Legacy
│
├── 📧 Phase 3: Email Extraction
│   └── 3_email_extractor/
│       ├── extract_emails_pro.py    ⭐ PRODUCTION
│       └── extract_emails.py        Legacy
│
├── ✉️ Phase 4: Email Sending
│   └── 4_email_sender/
│       ├── send_campaign_pro.py     ⭐ Gmail API (100/day)
│       ├── GoogleAppsScript.gs      ⭐ Workspace (1500/day)
│       └── send_campaign.py         Legacy
│
├── 🎨 Templates
│   └── templates/
│       ├── cold_email.html          ⭐ HTML template
│       └── default.txt              Plain text (legacy)
│
├── 📊 Data (Created at runtime)
│   └── data/
│       ├── raw_images/              Downloaded posts
│       ├── extracted_text/          OCR results
│       ├── leads.db                 SQLite database
│       ├── leads_export.csv         CSV export
│       ├── instagram_cookies.json   Login session
│       └── token.json               Gmail auth token
│
├── 📝 Logs (Created at runtime)
│   └── logs/
│       ├── scraper.log
│       ├── ocr.log
│       ├── email_extraction.log
│       └── email_campaign.log
│
└── 🤖 Workflows
    └── .agent/workflows/
        └── lead-gen-pipeline.md     Complete workflow

⭐ = Production-ready (use these)
⚠️ = Critical (must read before sending emails)
```

---

## 🎯 Quick Start Paths

### Path 1: Full Automated Setup (Recommended)
```bash
1. Read: GETTING_STARTED.md
2. Run:  python setup.py
3. Follow on-screen instructions
```

### Path 2: Manual Setup
```bash
1. Read: README.md
2. Follow: .agent/workflows/lead-gen-pipeline.md
3. Reference: QUICK_REFERENCE.md as needed
```

### Path 3: Google Apps Script Only (No Python)
```bash
1. Export leads from elsewhere (CSV)
2. Follow instructions in: 4_email_sender/GoogleAppsScript.gs
3. Set up in Google Sheets
```

---

## 📚 Documentation by Use Case

### "I'm just starting"
1. [GETTING_STARTED.md](GETTING_STARTED.md)
2. [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

### "I need to set this up"
1. `setup.py` (run this)
2. [.agent/workflows/lead-gen-pipeline.md](.agent/workflows/lead-gen-pipeline.md)

### "I'm stuck on something"
1. [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
2. `logs/` directory
3. [README.md](README.md) troubleshooting section

### "I need to stay legal"
1. [COMPLIANCE_CHECKLIST.md](COMPLIANCE_CHECKLIST.md) ⚠️ (CRITICAL)

### "I want to understand everything"
1. [README.md](README.md)
2. [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
3. Source code comments in `*_pro.py` files

---

## 🔢 File Count Summary

- **Documentation:** 7 files (50+ pages)
- **Configuration:** 4 files
- **Python Scripts:** 7 files (4 production, 3 legacy)
- **Google Apps Script:** 1 file
- **Templates:** 2 files
- **Workflows:** 1 file

**Total:** 22 files ready to use

---

## 🎓 Learning Path

### Beginner (2 hours)
1. Read GETTING_STARTED.md (30 min)
2. Run setup.py (30 min)
3. Test with 10 posts (1 hour)

### Intermediate (1 day)
1. Complete beginner path
2. Read COMPLIANCE_CHECKLIST.md (30 min)
3. Run pilot campaign - 50 leads (3 hours)
4. Study QUICK_REFERENCE.md (30 min)

### Advanced (1 week)
1. Complete intermediate path
2. Read all documentation (2 hours)
3. Run full campaign - 20k posts (automated, takes days)
4. Optimize based on metrics
5. Customize templates and scripts

---

## ⚡ Quick Command Reference

| What | Command |
|------|---------|
| **Setup** | `python setup.py` |
| **Scrape** | `python 1_scraper/instagram_scraper_pro.py` |
| **OCR** | `python 2_ocr/process_images_pro.py` |
| **Extract** | `python 3_email_extractor/extract_emails_pro.py` |
| **Send** | `python 4_email_sender/send_campaign_pro.py` |
| **Check DB** | `sqlite3 data/leads.db "SELECT COUNT(*) FROM leads"` |
| **View logs** | `type logs\email_campaign.log` |

---

## 🔐 Security Reminders

**Never commit these files to Git:**
- `.env`
- `credentials.json`
- `data/token.json`
- `data/instagram_cookies.json`
- `data/*.db`

**Protected by `.gitignore`** ✅

---

## 📞 Get Help

**Check in this order:**
1. Logs: `logs/*.log`
2. QUICK_REFERENCE.md
3. GETTING_STARTED.md (FAQ section)
4. README.md (Troubleshooting section)

**Still stuck?**
- Review error messages carefully
- Check your .env configuration
- Verify API keys are correct
- Make sure dependencies are installed

---

## ✅ Pre-Campaign Checklist

Before sending to real leads, ensure you've:

- [ ] Read GETTING_STARTED.md
- [ ] Completed COMPLIANCE_CHECKLIST.md
- [ ] Tested with 10 sample posts
- [ ] Customized email template
- [ ] Added business address to email
- [ ] Tested unsubscribe mechanism
- [ ] Sent test email to yourself
- [ ] Run pilot campaign (50 leads)
- [ ] Reviewed metrics from pilot

---

## 🎉 You Have Everything You Need!

- ✅ 7 comprehensive documentation files
- ✅ 4 production-ready Python scripts
- ✅ Google Apps Script for high-volume sending
- ✅ Professional HTML email template
- ✅ Automated setup script
- ✅ Complete workflow guides
- ✅ Legal compliance checklists
- ✅ Troubleshooting resources

**Next step:** Open [GETTING_STARTED.md](GETTING_STARTED.md) and begin! 🚀

---

**Updated:** November 27, 2025  
**Version:** 2.0 Production-Ready
