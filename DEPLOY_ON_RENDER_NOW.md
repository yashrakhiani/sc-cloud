# 🎉 CODE UPLOADED TO GITLAB! NOW DEPLOY ON RENDER

## ✅ STEP 1 COMPLETE!

Your code is now on GitLab: https://gitlab.com/yashr.otp-group/structcrew_leadgen

---

## 🚀 STEP 2: DEPLOY ON RENDER (3 MINUTES)

### Go to Render Dashboard

**Open**: https://dashboard.render.com

---

### Create Background Worker

1. Click **"New +"** button (top right)
2. Select **"Background Worker"**

---

### Connect GitLab

1. Click **"Connect GitLab"**
2. If not connected:
   - Click **"Connect GitLab"**
   - Authorize Render to access your GitLab
   - Sign in if needed
3. Select repository: **`structcrew_leadgen`**
4. Click **"Connect"**

---

### Configure Service

Fill in these settings:

**Name**: `structcrew-leadgen`

**Environment**: `Python 3`

**Build Command**:
```
pip install -r requirements.txt
```

**Start Command**:
```
python daily_runner.py
```

**Instance Type**: `Free`

---

### Add Environment Variables

Click **"Advanced"** button

Scroll down to **"Environment Variables"**

Click **"Add Environment Variable"** and add these **ONE BY ONE**:

| Key | Value |
|-----|-------|
| `INSTAGRAM_USERNAME` | `archijobs` |
| `INSTAGRAM_LOGIN_USER` | `brijeshrajan213` |
| `INSTAGRAM_LOGIN_PASS` | `Yashhk` |
| `GEMINI_API_KEY` | `AIzaSyACWNeMcb4xMCxm8BnSXFS9-S8loUAvEhY` |
| `FROM_EMAIL` | `structcrew@gmail.com` |
| `GMAIL_APP_PASSWORD` | `syjg ogsv wrab uoei` |
| `MAX_POSTS` | `500` |
| `DAILY_EMAIL_LIMIT` | `500` |
| `HEADLESS` | `true` |
| `USE_CLAUDE` | `false` |
| `VALIDATE_EMAILS` | `true` |

**⚠️ IMPORTANT**: 
- Type each value exactly as shown
- NO quotes around values
- Double-check `GMAIL_APP_PASSWORD` has no spaces

---

### Deploy!

1. Scroll to bottom
2. Click **"Create Background Worker"**
3. Wait 2-3 minutes for build

---

## 📊 MONITOR DEPLOYMENT

### During Build (2-3 minutes):
You'll see:
```
Installing dependencies...
Building...
Starting service...
```

### After Deployment:
Click **"Logs"** tab to see:
```
🚀 STARTING DAILY PIPELINE RUN
📸 Phase 1: Scraping Instagram (HTTP + Auth)...
🔍 Phase 2: Running OCR...
⛏️ Phase 3: Extracting Emails...
📧 Phase 4: Sending Emails...
✅ DAILY PIPELINE COMPLETE
```

---

## ✅ SUCCESS CHECKLIST

- [ ] Opened Render dashboard
- [ ] Created Background Worker
- [ ] Connected GitLab repository
- [ ] Set Build Command: `pip install -r requirements.txt`
- [ ] Set Start Command: `python daily_runner.py`
- [ ] Added ALL 11 environment variables
- [ ] Clicked "Create Background Worker"
- [ ] Service is deploying
- [ ] Logs show pipeline running

---

## 🎯 WHAT HAPPENS NEXT

Once deployed:
1. ✅ Pipeline runs immediately
2. ✅ Scrapes 500 Instagram posts
3. ✅ Extracts emails
4. ✅ Sends 500 emails
5. ✅ Sleeps for 24 hours
6. ✅ Repeats daily forever!

**Your laptop can stay closed!** ☕

---

## 📱 AFTER DEPLOYMENT

### Check Results:
- **Gmail Sent Folder**: See emails being sent
- **Render Logs**: Monitor pipeline activity
- **Database**: Growing with new leads daily

### Update Code:
```bash
# Make changes locally
git add .
git commit -m "Updated template"
python gitlab_upload.py  # Re-upload
```

Render will auto-redeploy! 🎉

---

## 🚀 READY?

**Go to**: https://dashboard.render.com

And follow the steps above!

**You're 3 minutes away from 24/7 automated lead generation!** 🎯

---

Need help with any step? Just ask! 💪
