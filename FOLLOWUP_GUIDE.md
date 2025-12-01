# 🔄 Follow-Up Campaign Guide

## What is This?

A system to automatically contact leads again after 15 or 30 days if they didn't respond.

---

## 📊 How It Works

### Lead Lifecycle:
```
Day 0:  Lead found → status='new'
        ↓
        Email sent → status='sent'
        ↓
Day 15: Follow-up #1 → status='followup_15'
        ↓
Day 30: Follow-up #2 → status='followup_30'
        ↓
        Done (or they replied!)
```

---

## 🚀 Usage

### Check Who's Ready for Follow-Up:
```bash
# Dry run (doesn't send, just shows who would get emails)
python followup_campaign.py 15 --dry-run
python followup_campaign.py 30 --dry-run
```

### Send 15-Day Follow-Up:
```bash
python followup_campaign.py 15
```

This will:
- Find all leads sent 15+ days ago
- Send a gentle reminder email
- Mark them as `status='followup_15'`

### Send 30-Day Follow-Up:
```bash
python followup_campaign.py 30
```

This will:
- Find all leads sent 30+ days ago (and not already followed up)
- Send a final "last chance" email
- Mark them as `status='followup_30'`

---

## 📧 Email Templates

### 15-Day Follow-Up:
**Subject**: "Still looking for architects?"

**Tone**: Helpful reminder
- Mentions you reached out before
- Highlights key benefits
- Offers quick chat

### 30-Day Follow-Up:
**Subject**: "Last chance to connect - StructCrew"

**Tone**: Final outreach
- States it's the last email
- Summarizes value proposition
- Gives them an easy out

---

## 📅 Recommended Schedule

### Manual Approach:
```bash
# Every Monday, run:
python followup_campaign.py 15
python followup_campaign.py 30
```

### Automated Approach:
Add to your daily runner or create a weekly cron job.

---

## 📊 Tracking Results

### Check Follow-Up Stats:
```bash
python check_results.py
```

This shows:
- How many at each status
- Total sent
- Ready for follow-up

### SQL Queries:

**See all follow-up candidates:**
```sql
SELECT company, email, sent_at, status 
FROM leads 
WHERE status='sent' 
AND DATE(sent_at) <= DATE('now', '-15 days');
```

**See follow-up success rate:**
```sql
SELECT status, COUNT(*) 
FROM leads 
GROUP BY status;
```

---

## 💡 Best Practices

### 1. Don't Over-Contact
- Max 3 emails total (initial + 2 follow-ups)
- Respect unsubscribe requests
- Give them space between emails

### 2. Track Responses
If someone replies:
```sql
UPDATE leads 
SET status='replied' 
WHERE email='their@email.com';
```

### 3. Clean Your List
After 30-day follow-up, mark as done:
```sql
UPDATE leads 
SET status='archived' 
WHERE status='followup_30' 
AND DATE(sent_at) < DATE('now', '-7 days');
```

---

## 🎯 Example Workflow

### Week 1:
```bash
# Daily: Scrape → Extract → Send to NEW leads
python daily_runner.py
```

### Week 3 (15 days later):
```bash
# Monday: Send 15-day follow-ups
python followup_campaign.py 15
```

### Week 5 (30 days later):
```bash
# Monday: Send 30-day follow-ups
python followup_campaign.py 30
```

---

## 📈 Expected Results

### Typical Response Rates:
- **Initial email**: 2-5% response rate
- **15-day follow-up**: 1-3% response rate
- **30-day follow-up**: 0.5-1% response rate

### Total Conversion:
With follow-ups, you can expect **3-9% total response rate** instead of just 2-5%.

**That's 50-80% more responses!** 🎉

---

## 🔧 Customization

### Change Follow-Up Timing:
Edit `followup_campaign.py`:
```python
# Instead of 15 days, use 10:
leads = get_followup_leads(days_ago=10)
```

### Change Email Templates:
Edit the templates in `followup_campaign.py`:
- `FOLLOWUP_15_TEMPLATE`
- `FOLLOWUP_30_TEMPLATE`

### Add More Follow-Ups:
You can add a 7-day follow-up or 45-day follow-up by copying the pattern.

---

## ⚠️ Important Notes

### Gmail Limits:
- 500 emails/day total (including follow-ups)
- If you send 500 initial emails, wait a day for follow-ups
- Or reduce initial emails to 400 to leave room for 100 follow-ups

### Database Integrity:
- Never manually change status to 'new' for already-sent leads
- Use follow-up system instead
- Keep backup of database

### Unsubscribes:
If someone unsubscribes:
```sql
UPDATE leads 
SET status='unsubscribed' 
WHERE email='their@email.com';
```

Then they won't get follow-ups.

---

## 🎓 Advanced: Automated Follow-Ups

### Option 1: Add to Daily Runner
Edit `daily_runner.py` to run follow-ups weekly:
```python
import schedule

# Run main pipeline daily
schedule.every().day.at("09:00").do(run_pipeline)

# Run follow-ups weekly (Monday at 10am)
schedule.every().monday.at("10:00").do(run_followup_15)
schedule.every().monday.at("10:30").do(run_followup_30)
```

### Option 2: Separate Cron Job
Create `weekly_followups.py`:
```python
from followup_campaign import run_followup_campaign

# Run both follow-ups
run_followup_campaign(days=15, dry_run=False)
run_followup_campaign(days=30, dry_run=False)
```

Then schedule it to run weekly.

---

## ✅ Quick Start

### 1. Test First:
```bash
python followup_campaign.py 15 --dry-run
```

### 2. Send Your First Follow-Up:
```bash
python followup_campaign.py 15
```

### 3. Monitor Results:
```bash
python check_results.py
```

### 4. Repeat Weekly:
Set a calendar reminder to run follow-ups every Monday.

---

## 📞 Support

Questions? Check:
- `YOUR_QUESTIONS_ANSWERED.md` - Database explanation
- `check_results.py` - See your lead stats
- Database directly: `data/leads.db`

---

**Start following up and get 50% more responses!** 🚀
