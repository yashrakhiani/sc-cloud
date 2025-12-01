# 🚀 DEPLOY ON RAILWAY - USE GITLAB DIRECTLY!

## ✅ YOUR GITLAB REPO IS PUBLIC!

**Repository**: https://gitlab.com/yashr.otp-group/structcrew_leadgen

Railway can deploy from this URL directly!

---

## 🎯 DEPLOY ON RAILWAY (2 MINUTES)

### Step 1: Go to Railway
**Open**: https://railway.app

### Step 2: Sign Up / Login
- Click **"Login"** or **"Start a New Project"**
- Sign in with email or GitHub

### Step 3: Deploy from Git URL

1. Click **"New Project"**
2. Click **"Deploy from GitHub repo"**
3. At the bottom, click **"Deploy from Git repository"** or **"Empty Service"**
4. If you see **"Empty Service"**, click it
5. Then click **"Settings"** → **"Connect Repo"**
6. Paste this URL: `https://gitlab.com/yashr.otp-group/structcrew_leadgen`

**OR**

1. Click **"Deploy from repo URL"** (if available)
2. Paste: `https://gitlab.com/yashr.otp-group/structcrew_leadgen`
3. Click **"Deploy"**

---

### Step 4: Configure Build

If Railway doesn't auto-detect, add these:

**Settings** → **Build**:
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python daily_runner.py`

---

### Step 5: Add Environment Variables

1. Click **"Variables"** tab
2. Click **"RAW Editor"**
3. Paste:

```
INSTAGRAM_USERNAME=archijobs
INSTAGRAM_LOGIN_USER=brijeshrajan213
INSTAGRAM_LOGIN_PASS=Yashhk
GEMINI_API_KEY=AIzaSyACWNeMcb4xMCxm8BnSXFS9-S8loUAvEhY
FROM_EMAIL=structcrew@gmail.com
GMAIL_APP_PASSWORD=syjg ogsv wrab uoei
MAX_POSTS=500
DAILY_EMAIL_LIMIT=500
HEADLESS=true
USE_CLAUDE=false
VALIDATE_EMAILS=true
```

4. Click **"Update Variables"**

---

### Step 6: Deploy!

Railway will automatically build and deploy!

Check **"Deployments"** → **Logs** to see it running!

---

## 🎯 ALTERNATIVE: Use Railway Template

Even easier:

1. Go to Railway
2. Click **"New Project"**
3. Click **"Empty Project"**
4. Click **"+ New"** → **"GitHub Repo"** or **"Empty Service"**
5. In Settings, connect to: `https://gitlab.com/yashr.otp-group/structcrew_leadgen`

---

## ✅ SUCCESS LOOKS LIKE:

```
Building...
Installing dependencies from requirements.txt
Starting service...
🚀 STARTING DAILY PIPELINE RUN
📸 Phase 1: Scraping Instagram...
```

---

## 🚀 READY?

**Go to**: https://railway.app

And deploy from your GitLab URL!

**Need help? Tell me what screen you're on and I'll guide you!** 💪
