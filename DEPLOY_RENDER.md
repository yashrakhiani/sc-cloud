# 🚀 Deploy to Render.com (FREE - 5 Minutes)

## Why Render?
- ✅ **100% Free** - No credit card required
- ✅ **750 hours/month** - Enough for 24/7 operation
- ✅ **Auto-deploy** - Push to GitHub, auto-updates
- ✅ **Built-in logging** - See what's happening
- ✅ **Easy setup** - Just click a few buttons

---

## 📋 Step-by-Step Deployment

### Step 1: Prepare Your Code (2 minutes)

First, let's create the necessary files for Render:

#### 1.1 Create `render.yaml` (already done for you!)

This file tells Render how to run your app.

#### 1.2 Create `requirements.txt` (already exists!)

Already configured with all dependencies.

#### 1.3 Create `.gitignore` (already exists!)

Ensures secrets aren't uploaded.

### Step 2: Push to GitHub (3 minutes)

```bash
# Initialize git (if not already done)
git init
git add .
git commit -m "Initial commit - Lead Gen Pipeline"

# Create a new repo on GitHub
# Then push:
git remote add origin https://github.com/YOUR_USERNAME/StructCrew_LeadGen.git
git branch -M main
git push -u origin main
```

### Step 3: Deploy on Render (2 minutes)

1. **Go to**: https://render.com
2. **Sign up** with GitHub (free, no credit card)
3. Click **"New +"** → **"Background Worker"**
4. Connect your GitHub repository
5. Configure:
   - **Name**: `structcrew-leadgen`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python daily_runner.py`
6. Click **"Advanced"** and add environment variables:
   ```
   INSTAGRAM_USERNAME=archijobs
   INSTAGRAM_LOGIN_USER=brijeshrajan213
   INSTAGRAM_LOGIN_PASS=Yashhk
   GEMINI_API_KEY=AIzaSyACWNeMcb4xMCxm8BnSXFS9-S8loUAvEhY
   FROM_EMAIL=structcrew@gmail.com
   GMAIL_APP_PASSWORD=syjg ogsv wrab uoei
   MAX_POSTS=200
   DAILY_EMAIL_LIMIT=200
   ```
7. Click **"Create Background Worker"**

### Step 4: Done! ✅

Your pipeline is now running 24/7 in the cloud!

---

## 📊 Monitor Your Pipeline

### View Logs:
1. Go to your Render dashboard
2. Click on your service
3. Click **"Logs"** tab
4. See real-time output!

### Check Results:
Your pipeline will:
- Run immediately on deployment
- Scrape 200 posts
- Send 200 emails
- Sleep for 24 hours
- Repeat daily at the same time

---

## 🔧 Update Your Pipeline

Just push to GitHub:
```bash
git add .
git commit -m "Updated email template"
git push
```

Render will automatically redeploy! 🎉

---

## ⚠️ Important Notes

### Free Tier Limitations:
- ✅ 750 hours/month (31 days × 24 hours = 744 hours)
- ✅ Enough for 24/7 operation
- ⚠️ Service sleeps after 15 min of inactivity
  - **Solution**: Our script runs continuously (24hr loop)

### Keeping It Alive:
The `daily_runner.py` already handles this by:
1. Running the pipeline
2. Sleeping for 24 hours (keeps process alive)
3. Repeating

This prevents Render from putting it to sleep!

---

## 🆓 Alternative: Railway.app (Even Easier!)

If you want something even simpler:

1. Go to: https://railway.app
2. Sign up with GitHub
3. Click **"New Project"** → **"Deploy from GitHub repo"**
4. Select your repo
5. Add environment variables (same as above)
6. Deploy!

**Note**: Railway requires a credit card but gives you $5/month free credit (won't charge).

---

## 🎯 What Happens After Deployment?

Your cloud server will:
1. ✅ Wake up at deployment
2. ✅ Run the pipeline (scrape → OCR → extract → email)
3. ✅ Sleep for 24 hours
4. ✅ Repeat daily forever

You can:
- Close your laptop ✅
- Turn off your computer ✅
- Go on vacation ✅
- Check logs anytime from your phone ✅

---

## 🔍 Troubleshooting

**"Service keeps restarting"**
- Check logs for errors
- Verify all environment variables are set

**"No emails being sent"**
- Check Gmail App Password is correct
- Verify leads exist in database

**"Instagram scraping fails"**
- Login credentials might be wrong
- Instagram might require 2FA (disable it)

---

## 📱 Next Steps

1. Push code to GitHub
2. Deploy on Render.com (5 min)
3. Check logs to verify it's running
4. Close your laptop and relax! ☕

**Your lead gen machine is now running 24/7 in the cloud!** 🚀

---

## 💡 Pro Tips

- **Monitor daily**: Check Render logs once a day
- **Database backup**: Download `data/leads.db` weekly
- **Email limits**: Start with 50/day, increase gradually
- **Instagram safety**: Don't exceed 500 posts/day

---

Need help? Check the logs first - they show everything!
