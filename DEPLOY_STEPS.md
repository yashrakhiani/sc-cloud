# 🚀 DEPLOY TO RENDER - STEP BY STEP (5 MINUTES)

You've created a Render account - Great! Now let's deploy.

---

## 📋 STEP 1: Push Your Code to GitHub (3 minutes)

### 1.1 Initialize Git Repository

Open your terminal in the project folder and run:

```bash
git init
```

### 1.2 Add All Files

```bash
git add .
```

### 1.3 Commit Your Code

```bash
git commit -m "Initial commit - StructCrew Lead Gen Pipeline"
```

### 1.4 Create GitHub Repository

1. Go to: https://github.com/new
2. Repository name: `StructCrew_LeadGen` (or any name)
3. Make it **Private** (recommended)
4. **DON'T** initialize with README (we already have code)
5. Click **"Create repository"**

### 1.5 Connect and Push

GitHub will show you commands. Use these:

```bash
git remote add origin https://github.com/YOUR_USERNAME/StructCrew_LeadGen.git
git branch -M main
git push -u origin main
```

**Replace `YOUR_USERNAME` with your GitHub username!**

---

## 📋 STEP 2: Deploy on Render (2 minutes)

### 2.1 Create New Service

1. Go to: https://dashboard.render.com
2. Click **"New +"** (top right)
3. Select **"Background Worker"**

### 2.2 Connect GitHub

1. Click **"Connect GitHub"**
2. Authorize Render to access your GitHub
3. Select your repository: `StructCrew_LeadGen`
4. Click **"Connect"**

### 2.3 Configure Service

Fill in these settings:

**Name**: `structcrew-leadgen` (or any name)

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

### 2.4 Add Environment Variables

Click **"Advanced"** → **"Add Environment Variable"**

Add these one by one:

```
INSTAGRAM_USERNAME = archijobs
INSTAGRAM_LOGIN_USER = brijeshrajan213
INSTAGRAM_LOGIN_PASS = Yashhk
GEMINI_API_KEY = AIzaSyACWNeMcb4xMCxm8BnSXFS9-S8loUAvEhY
FROM_EMAIL = structcrew@gmail.com
GMAIL_APP_PASSWORD = syjg ogsv wrab uoei
MAX_POSTS = 500
DAILY_EMAIL_LIMIT = 500
HEADLESS = true
USE_CLAUDE = false
VALIDATE_EMAILS = true
```

**Important**: No quotes around values!

### 2.5 Deploy!

1. Click **"Create Background Worker"**
2. Render will start building your service
3. Wait 2-3 minutes for deployment

---

## 📊 STEP 3: Verify It's Working (1 minute)

### 3.1 Check Logs

1. Click on your service
2. Click **"Logs"** tab
3. You should see:
   ```
   🚀 STARTING DAILY PIPELINE RUN
   📸 Phase 1: Scraping Instagram...
   ```

### 3.2 Monitor Progress

Watch the logs to see:
- Instagram scraping
- OCR processing
- Email extraction
- Emails being sent

### 3.3 Success!

When you see:
```
✅ DAILY PIPELINE COMPLETE
```

**You're done! Your pipeline is running in the cloud!** 🎉

---

## 🔧 TROUBLESHOOTING

### "Build failed"
- Check that `requirements.txt` exists
- Verify all files were pushed to GitHub

### "Service keeps restarting"
- Check logs for errors
- Verify environment variables are set correctly
- Make sure no quotes around variable values

### "Instagram login failed"
- Double-check `INSTAGRAM_LOGIN_USER` and `INSTAGRAM_LOGIN_PASS`
- Make sure 2FA is disabled on Instagram account

### "Gmail authentication failed"
- Verify `GMAIL_APP_PASSWORD` is correct (16 characters)
- No spaces in the password
- Regenerate if needed: https://myaccount.google.com/apppasswords

---

## 📱 AFTER DEPLOYMENT

### Monitor Your Service:
- Dashboard: https://dashboard.render.com
- Click on your service to see logs
- Check "Events" tab for deployment history

### Update Your Code:
```bash
# Make changes to your code
git add .
git commit -m "Updated email template"
git push
```

Render will **automatically redeploy**! 🎉

### Check Results:
- Your Gmail sent folder will have new emails
- Database grows with new leads
- Pipeline runs every 24 hours

---

## 🎯 QUICK CHECKLIST

Before deploying, make sure:

- [ ] Git is installed (`git --version`)
- [ ] GitHub account created
- [ ] Render account created (✅ You did this!)
- [ ] `.env` file has all credentials
- [ ] Ready to push to GitHub

---

## 💡 PRO TIPS

1. **Keep .env local**: Never push it to GitHub (already in `.gitignore`)
2. **Use Render dashboard**: Add/update environment variables there
3. **Monitor first 24 hours**: Check logs daily for first week
4. **Download database backup**: Weekly from Render dashboard

---

## 🚀 READY?

Follow the steps above and you'll be deployed in 5 minutes!

**Need help?** I'm here to guide you through each step! 🎯
