# 🚀 QUICK START: Deploy Your Lead Gen Pipeline to Cloud

## ⚡ TL;DR - Get Running in 5 Minutes

### Option 1: Render.com (NO CREDIT CARD) ⭐ RECOMMENDED
```bash
1. Push to GitHub
2. Go to render.com → Sign up with GitHub
3. New Background Worker → Select your repo
4. Add environment variables from .env
5. Deploy!
```
**Guide**: `DEPLOY_RENDER.md`

### Option 2: Railway.app (EASIEST) ⭐⭐ 
```bash
1. Push to GitHub
2. Go to railway.app → Sign up with GitHub  
3. New Project → Deploy from GitHub
4. Add environment variables
5. Done!
```
**Guide**: `DEPLOY_RAILWAY.md`

---

## 📊 Which One Should I Choose?

### Choose **Render.com** if:
- ✅ You don't have a credit card
- ✅ You want free forever
- ✅ You're okay with 5-minute setup

### Choose **Railway.app** if:
- ✅ You have a credit card (won't charge)
- ✅ You want the easiest experience
- ✅ You want the best dashboard

**Both work perfectly for your use case!**

---

## 🎯 What Your Pipeline Does (Automated)

```
Every 24 hours:
├── 📸 Scrape 200 Instagram posts (~10 min)
├── 🔍 Extract text with OCR (~5 min)
├── 📧 Find emails in text (~2 min)
└── ✉️ Send 200 personalized emails (~10 min)

Total: ~30 minutes per day
Sleep: 23.5 hours
```

---

## 📋 Pre-Deployment Checklist

Before deploying, make sure:

- [ ] `.env` file has all credentials
- [ ] Gmail App Password is set
- [ ] Instagram login works
- [ ] Gemini API key is valid
- [ ] Code is tested locally
- [ ] `.gitignore` includes `.env`

---

## 🔐 Environment Variables You'll Need

Copy these from your `.env` file:

```env
INSTAGRAM_USERNAME=archijobs
INSTAGRAM_LOGIN_USER=brijeshrajan213
INSTAGRAM_LOGIN_PASS=Yashhk
GEMINI_API_KEY=AIzaSyACWNeMcb4xMCxm8BnSXFS9-S8loUAvEhY
FROM_EMAIL=structcrew@gmail.com
GMAIL_APP_PASSWORD=syjg ogsv wrab uoei
MAX_POSTS=200
DAILY_EMAIL_LIMIT=200
```

**⚠️ IMPORTANT**: Never commit these to GitHub! They're already in `.gitignore`.

---

## 📁 Files You Need

All ready to go:
- ✅ `requirements.txt` - Python dependencies
- ✅ `daily_runner.py` - Main automation script
- ✅ `render.yaml` - Render config (optional)
- ✅ `.gitignore` - Protects secrets
- ✅ `Dockerfile` - For advanced deployments

---

## 🚀 Deployment Steps (Detailed)

### Step 1: Push to GitHub (2 minutes)

```bash
# If you haven't initialized git yet:
git init
git add .
git commit -m "Lead gen pipeline ready for cloud"

# Create a new repo on GitHub (github.com/new)
# Then connect and push:
git remote add origin https://github.com/YOUR_USERNAME/StructCrew_LeadGen.git
git branch -M main
git push -u origin main
```

### Step 2: Choose Your Cloud Platform

#### Option A: Render.com (Free Forever)
1. Go to https://render.com
2. Sign up with GitHub (no credit card)
3. Click "New +" → "Background Worker"
4. Select your GitHub repo
5. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python daily_runner.py`
6. Add environment variables (from above)
7. Click "Create Background Worker"

#### Option B: Railway.app (Easiest)
1. Go to https://railway.app
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repo
5. Go to "Variables" → "Raw Editor"
6. Paste environment variables (from above)
7. Click "Update Variables"

### Step 3: Monitor Deployment

Watch the logs to see:
```
🚀 STARTING DAILY PIPELINE RUN
📸 Phase 1: Scraping Instagram (HTTP + Auth)...
🔍 Phase 2: Running OCR...
⛏️ Phase 3: Extracting Emails...
📧 Phase 4: Sending Emails...
✅ DAILY PIPELINE COMPLETE
```

### Step 4: Verify It's Working

Check:
- ✅ Logs show successful completion
- ✅ Gmail sent folder has new emails
- ✅ No errors in logs

### Step 5: Close Your Laptop! ☕

Your pipeline is now running 24/7 in the cloud!

---

## 📊 Monitoring Your Pipeline

### Render.com:
- Dashboard → Your Service → Logs tab
- See real-time output
- Check for errors

### Railway.app:
- Dashboard → Your Service → Deployments
- Beautiful metrics dashboard
- Mobile app available!

---

## 🔧 Updating Your Pipeline

Made changes? Just push to GitHub:

```bash
git add .
git commit -m "Updated email template"
git push
```

Both Render and Railway will **auto-deploy** your changes! 🎉

---

## 💰 Cost Breakdown

### Render.com:
- **Free Tier**: 750 hours/month
- **Your Usage**: ~15 hours/month (30 min/day × 30 days)
- **Cost**: $0/month ✅

### Railway.app:
- **Free Credit**: $5/month
- **Your Usage**: ~$1-2/month
- **Cost**: $0/month (within free tier) ✅

**Both are completely free for your use case!**

---

## ⚠️ Common Issues

### "Instagram login failed"
- Check credentials in environment variables
- Disable 2FA on Instagram account
- Try logging in manually first

### "Gmail authentication failed"
- Verify Gmail App Password is correct
- Check it's 16 characters (no spaces)
- Regenerate if needed

### "No posts scraped"
- Instagram might be rate limiting
- Check if account is logged in
- Verify username is correct

### "Service keeps restarting"
- Check logs for Python errors
- Verify all dependencies in requirements.txt
- Check environment variables are set

---

## 📈 Scaling Up

Want to scrape more?

```env
# In your cloud dashboard, update:
MAX_POSTS=500              # Scrape 500 posts
DAILY_EMAIL_LIMIT=500      # Send 500 emails
```

**Safe limits**:
- Posts: Up to 1000/day
- Emails: Up to 500/day (Gmail free tier)

---

## 🎓 Next Steps After Deployment

1. **Week 1**: Monitor daily, check logs
2. **Week 2**: Verify email deliverability
3. **Week 3**: Increase limits gradually
4. **Week 4**: Set it and forget it! ✅

---

## 📞 Need Help?

1. **Check logs first** - Most issues show up there
2. **Read the guides**:
   - `DEPLOY_RENDER.md` - Render.com details
   - `DEPLOY_RAILWAY.md` - Railway.app details
   - `CLOUD_OPTIONS.md` - Compare all options
3. **Test locally** - Run `python daily_runner.py` first

---

## 🎉 You're Done!

Your lead generation machine is now:
- ✅ Running 24/7 in the cloud
- ✅ Scraping Instagram daily
- ✅ Sending personalized emails
- ✅ Completely automated

**Close your laptop and let it work for you!** 🚀

---

## 📱 Pro Tips

1. **Download Railway mobile app** - Monitor from phone
2. **Set up email alerts** - Get notified of issues
3. **Backup database weekly** - Download `leads.db`
4. **Start small** - 50 emails/day, then scale up
5. **Check spam folder** - Verify deliverability

---

**Ready to deploy?** Pick your platform and follow the guide! 🎯

- **No credit card?** → Use Render.com
- **Want easiest?** → Use Railway.app
- **Want comparison?** → Read `CLOUD_OPTIONS.md`
