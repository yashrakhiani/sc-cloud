# 🚀 Quick Start: Send Your First Campaign

## ✅ Your Configuration is Ready!

**Email**: structcrew@gmail.com  
**FROM_NAME**: StructCrew Team  
**Leads Ready**: 4 architecture studios

---

## 📋 Steps to Send Emails:

### Step 1: Create Gmail App Password

⚠️ **You MUST do this - regular password won't work!**

1. Go to: https://myaccount.google.com/apppasswords
2. Sign in with: `structcrew@gmail.com` / `Lolokok1`
3. Select app: **Mail**
4. Select device: **Windows Computer**
5. Click **Generate**
6. Copy the 16-character password (looks like: `abcd efgh ijkl mnop`)

### Step 2: Add App Password to .env

Open `.env` file and add this line:
```
GMAIL_APP_PASSWORD=your-16-character-password-here
```

### Step 3: Send Test Email

Run this command to send to **1 lead** only (test):
```bash
python send_emails_simple.py
```

This will:
- ✅ Send to 1 lead only (test mode)
- ✅ Show you exactly what's being sent
- ✅ Ask for confirmation before sending

### Step 4: Send to All Leads

Once test works, send to all 4 leads:
```bash
python send_emails_simple.py --live
```

---

## 📧 What You're Sending:

**Subject**: Architecture Collaboration Opportunity - [Company Name]

**Content**:
- Beautiful HTML email with gradient header
- Personalized with company name
- Professional StructCrew branding
- Clear value proposition
- Easy call-to-action button
- Unsubscribe option (legally required)

---

## 🎯 Your 4 Leads:

1. **AARNA VENTURES** - info@aarnaventures.in
2. **Interior Designer** - oneedgedesigns@gmail.com  
3. **CROMATICA** - nai@amail.com (may need verification)
4. **THIDAM WORKS** - thidamworks@amail.com (may need verification)

---

## ⚙️ Email Limits:

- **Test Mode**: 1 email per run
- **Live Mode**: 10 emails per day (configured in .env)
- **Gmail Free**: Maximum 100 emails/day
- **Recommended**: Start with 10-20/day to warm up

---

## 🔍 Track Results:

After sending, check your database:
```bash
python check_results.py
```

Or view in your inbox - recipients may reply!

---

## 🛡️ Safety Features:

✅ Test mode by default (sends only 1 email)  
✅ Confirmation required before sending  
✅ Rate limiting (2 seconds between emails)  
✅ Database tracking (won't send duplicates)  
✅ Error handling and logging  
✅ Unsubscribe option in every email

---

## ❌ Troubleshooting:

**"Invalid credentials"**:
- You're using regular password instead of App Password
- Create App Password at: https://myaccount.google.com/apppasswords

**"App Password link doesn't work"**:
- Enable 2-Step Verification first: https://myaccount.google.com/security
- Then try creating App Password again

**"No leads found"**:
- Run: `python 3_email_extractor/extract_emails_pro.py`
- Check: `data/leads_export.csv`

---

## 🚀 Ready Checklist:

- [ ] Created Gmail App Password
- [ ] Added `GMAIL_APP_PASSWORD` to `.env`
- [ ] Tested with 1 email: `python send_emails_simple.py`
- [ ] Checked test email in recipient's inbox
- [ ] Ready for full campaign: `python send_emails_simple.py --live`

---

**Need help?** Check `GMAIL_SETUP.md` for detailed Gmail configuration instructions.

**Let's get those leads! 💼**
