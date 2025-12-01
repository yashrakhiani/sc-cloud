# ✅ DEPLOYMENT CHECKLIST

Use this checklist to deploy your lead gen pipeline to the cloud in under 10 minutes!

---

## 📋 PRE-DEPLOYMENT (5 minutes)

### Step 1: Verify Local Setup
- [ ] Pipeline runs successfully locally
- [ ] `python daily_runner.py` works without errors
- [ ] Emails are being sent successfully
- [ ] Instagram scraper logs in correctly
- [ ] OCR is extracting text properly

### Step 2: Check Environment Variables
- [ ] `.env` file exists and has all values
- [ ] `INSTAGRAM_LOGIN_USER` is set
- [ ] `INSTAGRAM_LOGIN_PASS` is set
- [ ] `GEMINI_API_KEY` is set
- [ ] `GMAIL_APP_PASSWORD` is set (16 characters)
- [ ] `FROM_EMAIL` is set

### Step 3: Verify Files
- [ ] `requirements.txt` exists
- [ ] `daily_runner.py` exists
- [ ] `.gitignore` includes `.env`
- [ ] All scraper files are present
- [ ] All email templates are present

---

## 🚀 DEPLOYMENT (5 minutes)

### Step 4: Push to GitHub
- [ ] Git is initialized (`git init`)
- [ ] All files are added (`git add .`)
- [ ] Committed (`git commit -m "Ready for deployment"`)
- [ ] Created GitHub repo
- [ ] Added remote (`git remote add origin ...`)
- [ ] Pushed to GitHub (`git push -u origin main`)

### Step 5: Choose Cloud Platform

#### Option A: Render.com (No Credit Card)
- [ ] Signed up at render.com
- [ ] Clicked "New Background Worker"
- [ ] Selected GitHub repo
- [ ] Set build command: `pip install -r requirements.txt`
- [ ] Set start command: `python daily_runner.py`
- [ ] Added all environment variables
- [ ] Clicked "Create Background Worker"

#### Option B: Railway.app (Easiest)
- [ ] Signed up at railway.app
- [ ] Clicked "New Project"
- [ ] Selected "Deploy from GitHub repo"
- [ ] Selected your repo
- [ ] Went to "Variables" tab
- [ ] Added all environment variables
- [ ] Service auto-deployed

---

## 🔍 POST-DEPLOYMENT (2 minutes)

### Step 6: Verify Deployment
- [ ] Deployment shows "Live" or "Running"
- [ ] No errors in build logs
- [ ] Service started successfully
- [ ] Can see logs in dashboard

### Step 7: Monitor First Run
- [ ] Logs show "STARTING DAILY PIPELINE RUN"
- [ ] Instagram scraping starts
- [ ] OCR processing completes
- [ ] Email extraction works
- [ ] Emails are being sent
- [ ] Pipeline completes successfully

### Step 8: Verify Results
- [ ] Check Gmail sent folder for new emails
- [ ] Verify emails look correct
- [ ] Check logs for any errors
- [ ] Confirm pipeline is sleeping (waiting 24 hours)

---

## 🎯 FINAL CHECKS

### Step 9: Long-term Setup
- [ ] Bookmarked cloud dashboard
- [ ] Set up email notifications (optional)
- [ ] Downloaded mobile app (Railway only)
- [ ] Tested updating via git push
- [ ] Documented any custom changes

### Step 10: Optimization
- [ ] Verified email deliverability (check spam)
- [ ] Adjusted daily limits if needed
- [ ] Set up database backup routine
- [ ] Planned weekly monitoring schedule

---

## 📊 ENVIRONMENT VARIABLES CHECKLIST

Copy these to your cloud dashboard:

```env
✅ INSTAGRAM_USERNAME=archijobs
✅ INSTAGRAM_LOGIN_USER=brijeshrajan213
✅ INSTAGRAM_LOGIN_PASS=Yashhk
✅ GEMINI_API_KEY=AIzaSyACWNeMcb4xMCxm8BnSXFS9-S8loUAvEhY
✅ FROM_EMAIL=structcrew@gmail.com
✅ GMAIL_APP_PASSWORD=syjg ogsv wrab uoei
✅ MAX_POSTS=200
✅ DAILY_EMAIL_LIMIT=200
✅ HEADLESS=true
✅ USE_CLAUDE=false
✅ VALIDATE_EMAILS=true
```

---

## ⚠️ COMMON ISSUES CHECKLIST

If something goes wrong, check:

### Build Fails:
- [ ] `requirements.txt` is correct
- [ ] Python version is compatible (3.9+)
- [ ] All dependencies are listed

### Service Crashes:
- [ ] All environment variables are set
- [ ] No typos in variable names
- [ ] Values don't have quotes (unless needed)

### Instagram Fails:
- [ ] Login credentials are correct
- [ ] 2FA is disabled on Instagram
- [ ] Account is not rate limited

### Email Fails:
- [ ] Gmail App Password is correct (16 chars)
- [ ] FROM_EMAIL matches Gmail account
- [ ] Not exceeding Gmail limits (500/day)

### No Leads Found:
- [ ] Instagram scraper ran successfully
- [ ] OCR extracted text
- [ ] Text contains email addresses
- [ ] Database file exists

---

## 🎓 TROUBLESHOOTING STEPS

1. **Check Logs First**
   - [ ] Read error messages carefully
   - [ ] Look for specific line numbers
   - [ ] Check timestamps

2. **Verify Environment**
   - [ ] All variables are set
   - [ ] No extra spaces in values
   - [ ] Correct variable names

3. **Test Locally**
   - [ ] Run same command locally
   - [ ] See if error reproduces
   - [ ] Fix locally first

4. **Restart Service**
   - [ ] Sometimes a simple restart helps
   - [ ] Redeploy if needed
   - [ ] Check logs after restart

---

## 📱 MONITORING CHECKLIST

### Daily (First Week):
- [ ] Check logs for errors
- [ ] Verify emails were sent
- [ ] Check Gmail sent folder
- [ ] Monitor deliverability

### Weekly (After First Week):
- [ ] Review total emails sent
- [ ] Check for any failures
- [ ] Download database backup
- [ ] Verify service is running

### Monthly:
- [ ] Review overall performance
- [ ] Adjust limits if needed
- [ ] Rotate API keys (security)
- [ ] Check cloud usage/credits

---

## 🎉 SUCCESS CRITERIA

You're done when:
- ✅ Service is deployed and running
- ✅ Logs show successful pipeline runs
- ✅ Emails are being sent daily
- ✅ No errors in logs
- ✅ You can close your laptop
- ✅ Pipeline runs automatically

---

## 📞 HELP RESOURCES

If stuck, check:
1. [ ] `DEPLOY_RENDER.md` - Render guide
2. [ ] `DEPLOY_RAILWAY.md` - Railway guide
3. [ ] `CLOUD_OPTIONS.md` - Compare options
4. [ ] `FREE_CLOUD_SUMMARY.md` - Quick reference
5. [ ] Cloud platform docs
6. [ ] Service logs (most helpful!)

---

## 🚀 READY TO DEPLOY?

### Quick Start:
1. ✅ Complete Pre-Deployment checklist
2. ✅ Push to GitHub
3. ✅ Deploy to Render or Railway
4. ✅ Verify it's working
5. ✅ Close your laptop!

**Time Required**: 10-15 minutes total

**Result**: 24/7 automated lead generation! 🎯

---

## 💡 PRO TIPS

- [ ] Start with 50 emails/day, scale up gradually
- [ ] Monitor first 3 days closely
- [ ] Keep a backup of your `.env` file (locally only!)
- [ ] Test email deliverability before scaling
- [ ] Set calendar reminder to check weekly

---

**Print this checklist and check off items as you go!** ✅

Good luck with your deployment! 🚀
