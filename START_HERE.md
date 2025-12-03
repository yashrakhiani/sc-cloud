# 🚀 START HERE: Deploy 500 Posts + 500 Emails Daily

## Your Goal
- ✅ Download 500 unique Instagram posts every day (automated)
- ✅ Extract emails from posts (automated)  
- ✅ Send 500 emails every day (automated)
- ✅ Run in cloud 24/7 with zero manual work

**Good news:** Everything is already built. Just deploy it.

---

## 3 Step Deployment

### Step 1: Prepare (2 minutes)
Edit `.env` file with your credentials:
```bash
INSTAGRAM_LOGIN_USER=your_username
INSTAGRAM_LOGIN_PASS=your_password
FROM_EMAIL=your-email@gmail.com
GMAIL_APP_PASSWORD=your_app_password  # Get from Gmail security settings
CLAUDE_API_KEY=your_key  # From console.anthropic.com
```

### Step 2: Test Locally (5 minutes)
```bash
python automation_manager.py
```
You'll see logs like:
```
🚀 STARTING DAILY AUTOMATION PIPELINE
🌍 PHASE 1: INSTAGRAM SCRAPER (500 posts)
🔍 PHASE 2: OCR TEXT EXTRACTION
⛏️ PHASE 3: EMAIL EXTRACTION
📧 PHASE 4: EMAIL CAMPAIGN (500 emails)
✅ DAILY PIPELINE COMPLETE
```

### Step 3: Deploy to Cloud (5-10 minutes)

**Choose ONE cloud platform:**

#### 🟢 Google Cloud (FREE forever)
```bash
1. Create VM at console.cloud.google.com (e2-micro)
2. SSH into it
3. Create 2GB swap: 
   sudo fallocate -l 2G /swapfile
   sudo chmod 600 /swapfile
   sudo mkswap /swapfile
   sudo swapon /swapfile
4. git clone your-repo
5. nano .env  (add credentials)
6. docker build -t leadgen .
7. docker run -d --restart always -v $(pwd)/data:/app/data leadgen
```

#### 🔵 Railway.app (Easiest)
```bash
1. Go to railway.app
2. New Project → Deploy from GitHub
3. Select your repo
4. Add env variables
5. Deploy (done in 1 minute!)
```

#### 🟡 Render (Reliable)
```bash
1. Go to render.com
2. New Web Service → GitHub
3. Build: pip install -r requirements.txt
4. Start: python automation_manager.py
5. Add env vars
6. Deploy
```

---

## What Happens Daily (Automated)

```
2:00 AM UTC  → Downloads 500 Instagram posts (2-3 hours)
4:00 AM UTC  → Extracts text from images (1-2 hours)
5:00 AM UTC  → Finds emails in text (30 minutes)
9:00 AM UTC  → Sends 500 emails
```

That's it. Every single day. No manual work.

---

## Check It's Working

After 24 hours, look for:
- New images in `data/raw_images/` 
- Extracted text in `data/extracted_text/`
- New rows in database

**Quick check:**
```bash
sqlite3 data/leads.db "SELECT COUNT(*) FROM emails WHERE date(sent_at)=date('now')"
```

Should show emails increasing each day.

---

## Expected Results

**First 24 hours:** 500 posts + 500 emails  
**First week:** 3,500 posts + 3,500 emails sent  
**First month:** 15,000 posts + 15,000 emails sent  
**First year:** 180,000 posts + 50,000 emails sent  

**Response rate:** 2-5% = **1,000-2,500 qualified leads per year**

---

## Cost

- Google Cloud: $0/month
- Claude API: $10-30/month (OCR)
- Gmail: $0-6/month
- **Total: $10-36/month**

---

## Need Details?

- **Quick start:** Read `AUTOMATE_NOW.md`
- **Full setup guide:** Read `CLOUD_AUTOMATION_SETUP.md`  
- **Step-by-step deployment:** Read `DEPLOY_CLOUD_NOW.md`
- **Complete overview:** Read `AUTOMATION_SUMMARY.md`

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Instagram blocks me | Increase delays in .env: `SCROLL_DELAY=5,15` |
| Can't send emails | Check Gmail app password |
| Out of memory (Google Cloud) | Create swap file |
| Not sure it's working | Check `logs/automation_manager.log` |

---

## Let's Do This! 🎯

**Right now:**

1. Update `.env` with credentials
2. Run `python automation_manager.py` to test
3. Pick a cloud platform (Railway = easiest)
4. Deploy using the steps above
5. Done! Check logs in 24 hours

**In 24 hours you'll have:**
- 500 new Instagram posts downloaded
- 200-300 emails extracted  
- 500 emails sent
- Everything automated and repeating daily

---

## Questions?

**Issue:** Container won't start  
**Fix:** Check logs - `docker logs automation`

**Issue:** Emails not sending  
**Fix:** Verify Gmail app password in .env

**Issue:** Not seeing new data  
**Fix:** Wait 24 hours for first automation run

**Still stuck?** Check `DEPLOY_CLOUD_NOW.md` troubleshooting section.

---

**Deploy now and you're done! The system runs itself. 🚀**
