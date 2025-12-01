# ⚠️ FIX: Gmail App Password Not Found

## THE PROBLEM

Railway can't see the `GMAIL_APP_PASSWORD` environment variable.

The `.env` file is NOT uploaded to GitHub (it's in `.gitignore` for security).

Railway needs you to set environment variables in its dashboard!

---

## ✅ SOLUTION: Set Variables in Railway Dashboard

### Step 1: Go to Railway

1. Open: https://railway.app
2. Click on your project
3. Click on your service (the one that's running)

### Step 2: Open Variables Tab

1. Look at the left sidebar
2. Click **"Variables"** (looks like a list icon)

### Step 3: Add the Gmail App Password

You'll see a list of variables. You need to add or update:

**Click "New Variable" or "RAW Editor"**

If using **RAW Editor**, paste this entire block:

```
INSTAGRAM_USERNAME=archijobs
INSTAGRAM_LOGIN_USER=brijeshrajan213
INSTAGRAM_LOGIN_PASS=Yashhk
GEMINI_API_KEY=AIzaSyACWNeMcb4xMCxm8BnSXFS9-S8loUAvEhY
FROM_EMAIL=structcrew@gmail.com
GMAIL_APP_PASSWORD=wqdy xnsf zwel kexh
MAX_POSTS=500
DAILY_EMAIL_LIMIT=500
HEADLESS=true
USE_CLAUDE=false
VALIDATE_EMAILS=true
FROM_NAME=StructCrew Team
```

If adding **one by one**:

Click **"New Variable"** for each:

1. **Variable name**: `GMAIL_APP_PASSWORD`
   **Value**: `wqdy xnsf zwel kexh`

2. **Variable name**: `DAILY_EMAIL_LIMIT`
   **Value**: `500`

3. **Variable name**: `MAX_POSTS`
   **Value**: `500`

### Step 4: Save

Railway will automatically restart your service!

---

## 🔍 VERIFY IT WORKED

### Check the Logs:

1. Click **"Deployments"** tab
2. Click on the latest deployment
3. Look for:

```
✅ Gmail App Password is SET (19 characters)
📧 Phase 4: Sending Emails...
📧 Sending to Company (email@example.com)...
   ✅ Sent successfully!
```

If you still see:
```
⚠️  GMAIL APP PASSWORD NOT CONFIGURED!
```

Then the variable wasn't set correctly.

---

## 📸 WHAT YOU SHOULD SEE IN RAILWAY:

### Variables Tab:
```
GMAIL_APP_PASSWORD    wqdy xnsf zwel kexh
DAILY_EMAIL_LIMIT     500
FROM_EMAIL            structcrew@gmail.com
GEMINI_API_KEY        AIzaSy... (masked)
...
```

---

## ⚠️ COMMON MISTAKES:

❌ **Adding spaces**: `wqdy xnsf zwel kexh` (correct)
❌ **Adding quotes**: `"wqdy xnsf zwel kexh"` (wrong!)
❌ **Wrong variable name**: `GMAIL_PASSWORD` (wrong!)
✅ **Correct**: `GMAIL_APP_PASSWORD=wqdy xnsf zwel kexh`

---

## 🎯 STEP-BY-STEP CHECKLIST:

- [ ] Opened Railway dashboard
- [ ] Clicked on my service
- [ ] Clicked "Variables" tab
- [ ] Added `GMAIL_APP_PASSWORD` with value `wqdy xnsf zwel kexh`
- [ ] Added `DAILY_EMAIL_LIMIT` with value `500`
- [ ] Service restarted automatically
- [ ] Checked logs - emails are being sent!

---

## 🚀 AFTER FIXING:

Your pipeline will:
1. ✅ Scrape 500 Instagram posts
2. ✅ Extract emails
3. ✅ **Send 500 emails** (this will work now!)
4. ✅ Sleep for 24 hours
5. ✅ Repeat daily

---

## 💡 NEED HELP?

Tell me:
1. Did you find the "Variables" tab in Railway?
2. Can you see other variables listed there?
3. Did you add `GMAIL_APP_PASSWORD`?

I'll help you through it! 🎯
