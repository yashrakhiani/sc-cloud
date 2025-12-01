# 🚂 Deploy to Railway.app (EASIEST - 3 Minutes)

## Why Railway?
- ✅ **Easiest deployment** - Literally 3 clicks
- ✅ **$5/month free credit** - ~500 hours of runtime
- ✅ **Never sleeps** - Always running
- ✅ **Beautiful dashboard** - Best UI
- ✅ **Instant logs** - Real-time monitoring

**Note**: Requires credit card (but won't charge unless you exceed free tier)

---

## 🚀 3-Minute Deployment

### Step 1: Push to GitHub (2 minutes)

```bash
# Initialize git (if not already done)
git init
git add .
git commit -m "Lead gen pipeline ready for deployment"

# Create a new repo on GitHub
# Then push:
git remote add origin https://github.com/YOUR_USERNAME/StructCrew_LeadGen.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy on Railway (1 minute!)

1. **Go to**: https://railway.app
2. **Sign up** with GitHub
3. Click **"New Project"**
4. Click **"Deploy from GitHub repo"**
5. Select `StructCrew_LeadGen`
6. Railway will auto-detect Python and deploy!

### Step 3: Add Environment Variables (30 seconds)

1. Click on your deployed service
2. Go to **"Variables"** tab
3. Click **"Raw Editor"**
4. Paste this:

```env
INSTAGRAM_USERNAME=archijobs
INSTAGRAM_LOGIN_USER=brijeshrajan213
INSTAGRAM_LOGIN_PASS=Yashhk
GEMINI_API_KEY=AIzaSyACWNeMcb4xMCxm8BnSXFS9-S8loUAvEhY
FROM_EMAIL=structcrew@gmail.com
GMAIL_APP_PASSWORD=syjg ogsv wrab uoei
MAX_POSTS=200
DAILY_EMAIL_LIMIT=200
HEADLESS=true
USE_CLAUDE=false
VALIDATE_EMAILS=true
```

5. Click **"Update Variables"**

### Step 4: Done! ✅

Railway will automatically restart with your variables!

---

## 📊 Monitor Your Pipeline

### View Logs:
1. Click on your service
2. Click **"Deployments"** tab
3. Click on the latest deployment
4. See real-time logs! 🎉

### Check Metrics:
- **CPU usage**
- **Memory usage**
- **Network traffic**
- **Deployment history**

All in a beautiful dashboard!

---

## 💰 Free Tier Details

### What You Get:
- **$5 credit/month** (free)
- **~500 hours** of runtime
- **512MB RAM**
- **1GB disk space**

### How Long Will It Last?
- **24/7 operation**: ~20 days
- **12 hours/day**: Full month
- **Once per day (1 hour)**: Full month + extra

### For Your Use Case:
Your pipeline runs:
1. Scrapes for ~10 minutes
2. Processes for ~5 minutes  
3. Sends emails for ~5 minutes
4. Sleeps for 24 hours

**Total**: ~20 minutes per day = **Full month coverage!** ✅

---

## 🔧 Update Your Pipeline

Just push to GitHub:
```bash
git add .
git commit -m "Updated scraper"
git push
```

Railway auto-deploys! No manual steps needed! 🎉

---

## 📱 Mobile App

Railway has a mobile app!
- Monitor logs from your phone
- Check deployment status
- View metrics
- Restart services

Download: https://railway.app/mobile

---

## 🎯 What Happens After Deployment?

Your cloud server will:
1. ✅ Start immediately
2. ✅ Run the pipeline (scrape → OCR → extract → email)
3. ✅ Sleep for 24 hours (keeps process alive)
4. ✅ Repeat daily forever

You can:
- Close your laptop ✅
- Turn off your computer ✅
- Monitor from your phone ✅
- Check logs anytime ✅

---

## 🔍 Troubleshooting

### "Service keeps crashing"
- Check logs for errors
- Verify environment variables are set correctly

### "Out of credits"
- You're using more than $5/month
- Options:
  1. Add payment method (pay-as-you-go)
  2. Optimize to run less frequently
  3. Switch to Render.com (free forever)

### "Deployment failed"
- Check `requirements.txt` is correct
- Verify Python version compatibility
- Check logs for specific error

---

## 💡 Pro Tips

### Optimize for Free Tier:
```python
# In daily_runner.py, you can adjust schedule:
schedule.every().day.at("09:00").do(run_pipeline)  # Run once per day
```

This keeps you well within the free tier!

### Monitor Usage:
1. Go to **"Usage"** tab
2. See credit consumption
3. Adjust frequency if needed

### Set Up Alerts:
1. Go to **"Settings"**
2. Enable **"Deployment notifications"**
3. Get notified of issues via email

---

## 🆚 Railway vs Render

| Feature | Railway | Render |
|---------|---------|--------|
| **Free Tier** | $5 credit | 750 hours |
| **Credit Card** | Required | Not required |
| **Sleeps?** | Never | After 15 min |
| **Dashboard** | Beautiful | Good |
| **Setup** | 3 min | 5 min |
| **Best For** | Easiest | No credit card |

**Choose Railway if**: You have a credit card and want the easiest experience
**Choose Render if**: You don't have a credit card

---

## 🔒 Security

Railway is secure:
- ✅ Environment variables encrypted
- ✅ HTTPS by default
- ✅ Private by default
- ✅ SOC 2 compliant

Your credentials are safe!

---

## 📈 Scaling

If you outgrow the free tier:

### Hobby Plan ($5/month):
- $5 credit + pay-as-you-go
- More resources
- Priority support

### Pro Plan ($20/month):
- $20 credit included
- Team features
- Advanced metrics

But for 200 posts/day, **free tier is enough!**

---

## 🎓 Next Steps

1. ✅ Push code to GitHub
2. ✅ Deploy on Railway (3 min)
3. ✅ Add environment variables
4. ✅ Check logs to verify it's running
5. ✅ Download mobile app
6. ✅ Close your laptop! ☕

**Your lead gen machine is now running 24/7!** 🚀

---

## 📞 Support

- **Docs**: https://docs.railway.app
- **Discord**: https://discord.gg/railway
- **Twitter**: @Railway

Railway has amazing community support!

---

## 🎉 Bonus: One-Click Deploy

Railway supports one-click deploy buttons!

Click this to deploy instantly:

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https://github.com/YOUR_USERNAME/StructCrew_LeadGen)

(Update the URL with your GitHub repo after pushing)

---

**Ready to deploy?** Go to https://railway.app and get started! 🚂
