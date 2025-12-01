# ✅ STEP 1 COMPLETE! Now Do This:

## 🎉 Your code is ready to push!

I've already done these for you:
- ✅ `git init` - Initialized repository
- ✅ `git add .` - Added all files
- ✅ `git commit` - Committed your code

---

## 📋 NEXT: Push to GitHub (2 minutes)

### Step 1: Create GitHub Repository

1. **Open**: https://github.com/new
2. **Repository name**: `StructCrew_LeadGen`
3. **Privacy**: Choose **Private** (recommended)
4. **Important**: **DON'T** check "Add a README file"
5. Click **"Create repository"**

### Step 2: Copy These Commands

After creating the repo, GitHub will show you commands.

**Run these in your terminal:**

```bash
git remote add origin https://github.com/YOUR_USERNAME/StructCrew_LeadGen.git
git branch -M main
git push -u origin main
```

**⚠️ IMPORTANT**: Replace `YOUR_USERNAME` with your actual GitHub username!

**Example**: If your GitHub username is `john123`, use:
```bash
git remote add origin https://github.com/john123/StructCrew_LeadGen.git
```

---

## 📋 THEN: Deploy on Render (3 minutes)

### Step 1: Go to Render Dashboard

**Open**: https://dashboard.render.com

### Step 2: Create Background Worker

1. Click **"New +"** button (top right)
2. Select **"Background Worker"**
3. Click **"Connect GitHub"** (if not connected)
4. Authorize Render
5. Select repository: `StructCrew_LeadGen`
6. Click **"Connect"**

### Step 3: Configure Settings

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

### Step 4: Add Environment Variables

Click **"Advanced"** → Scroll to **"Environment Variables"**

Click **"Add Environment Variable"** and add these **one by one**:

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
- No quotes around values!
- Copy-paste exactly as shown
- Double-check `GMAIL_APP_PASSWORD` (no spaces)

### Step 5: Deploy!

1. Click **"Create Background Worker"**
2. Wait 2-3 minutes for build
3. Check **"Logs"** tab to see it running

---

## 🎯 WHAT TO EXPECT

### During Build (2-3 minutes):
```
Installing dependencies...
Building...
Starting service...
```

### After Deployment:
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

- [ ] Created GitHub repository
- [ ] Pushed code to GitHub
- [ ] Connected Render to GitHub
- [ ] Created Background Worker
- [ ] Added all environment variables
- [ ] Service is deployed and running
- [ ] Logs show pipeline running
- [ ] Emails are being sent!

---

## 🚀 YOU'RE ALMOST THERE!

Just 2 more steps:
1. **Push to GitHub** (2 min)
2. **Deploy on Render** (3 min)

**Total time**: 5 minutes to automated lead generation! 🎉

---

## 💡 NEED HELP?

If you get stuck:
1. Check `DEPLOY_STEPS.md` for detailed guide
2. Check Render logs for errors
3. Verify environment variables are set correctly

**Let's do this!** 🚀
