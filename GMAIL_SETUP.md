# 📧 Gmail Setup Instructions for StructCrew Email Campaigns

## ⚠️ Important: Gmail Security Update

Gmail **no longer allows** direct password authentication for security reasons. You need to create an **App Password**.

---

## 🔧 Step-by-Step Setup:

### Option 1: Gmail App Password (Easiest - 5 minutes)

1. **Enable 2-Step Verification** (if not already enabled):
   - Go to: https://myaccount.google.com/security
   - Click "2-Step Verification"
   - Follow the setup process

2. **Create an App Password**:
   - Go to: https://myaccount.google.com/apppasswords
   - Select app: "Mail"
   - Select device: "Windows Computer"
   - Click "Generate"
   - **Copy the 16-character password** (example: `abcd efgh ijkl mnop`)

3. **Update the email sender script** with your App Password

---

### Option 2: Gmail API with OAuth2 (More Secure, Recommended for Production)

This method is more complex but more secure and allows higher sending limits.

1. **Enable Gmail API**:
   - Go to: https://console.cloud.google.com/
   - Create new project: "StructCrew-Email"
   - Enable Gmail API
   - Create OAuth 2.0 credentials (Desktop app)
   - Download as `credentials.json`

2. **First Run Authentication**:
   - Run the email sending script
   - Browser will open for authentication
   - Grant permissions
   - Token will be saved for future use

---

## 🚀 Quick Start with App Password

I'll create a simple SMTP-based email sender that works with Gmail App Passwords.

**Your Current Info:**
- Email: `structcrew@gmail.com`
- Password: `Lolokok1` ❌ (Won't work - need App Password)

**Next Steps:**
1. Create Gmail App Password (see above)
2. I'll create a simple email sender script
3. Test with 1 email first
4. Then send to all 4 leads!

---

## 📊 Email Sending Limits

- **Free Gmail**: 100 emails/day
- **Google Workspace**: 1,500 emails/day
- **Recommended**: Start with 10-20 emails/day to warm up your domain

---

**Ready to proceed?** 
- Get your Gmail App Password, then I'll  create the automated email sender!
