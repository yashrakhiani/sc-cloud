# 🔍 Monitoring & Maintenance Guide

Monitor your cloud automation and optimize performance over time.

---

## Daily Monitoring (2 minutes)

### Check Status
```bash
# View latest logs
tail -30 logs/automation_manager.log

# See current state
cat data/automation_state.json
```

**Look for:**
- ✅ No error messages
- ✅ Phases completed successfully
- ✅ Timestamps progressing

### Expected Daily Output
```json
{
  "last_scrape_date": "2025-12-04T02:00:00",
  "posts_scraped_today": 500,
  "emails_sent_today": 500,
  "last_successful_run": "2025-12-04T09:30:00",
  "current_phase": "idle"
}
```

---

## Weekly Monitoring (10 minutes)

### Email Metrics
```bash
# Emails sent this week
sqlite3 data/leads.db "SELECT COUNT(*) FROM emails WHERE date(sent_at) >= date('now', '-7 days') AND status='sent'"

# Emails still pending
sqlite3 data/leads.db "SELECT COUNT(*) FROM emails WHERE status='pending'"

# Bounced emails
sqlite3 data/leads.db "SELECT COUNT(*) FROM emails WHERE status='bounced'"

# Responses received
sqlite3 data/leads.db "SELECT COUNT(*) FROM emails WHERE status='replied'"
```

### Database Health
```bash
# Total size
du -sh data/

# Posts collected
sqlite3 data/leads.db "SELECT COUNT(*) FROM raw_posts"

# Unique emails
sqlite3 data/leads.db "SELECT COUNT(DISTINCT email) FROM emails"

# Database integrity
sqlite3 data/leads.db "PRAGMA integrity_check"
```

### Log Analysis
```bash
# Errors in past week
grep -i error logs/automation_manager.log | tail -20

# Success rate
grep "DAILY PIPELINE COMPLETE" logs/automation_manager.log | wc -l

# Failed phases
grep "❌" logs/automation_manager.log | tail -10
```

---

## Monthly Review (30 minutes)

### Performance Metrics
```bash
# This month's data
sqlite3 data/leads.db << EOF
SELECT 
  DATE(created_at) as date,
  COUNT(*) as posts
FROM raw_posts
WHERE strftime('%Y-%m', created_at) = strftime('%Y-%m', 'now')
GROUP BY DATE(created_at)
ORDER BY date DESC
EOF

# Email sending rate
sqlite3 data/leads.db << EOF
SELECT 
  DATE(sent_at) as date,
  COUNT(*) as emails
FROM emails
WHERE strftime('%Y-%m', sent_at) = strftime('%Y-%m', 'now')
GROUP BY DATE(sent_at)
ORDER BY date DESC
EOF
```

### Deliverability Analysis
```bash
# Response rate
echo "scale=2; $(sqlite3 data/leads.db "SELECT COUNT(*) FROM emails WHERE status='replied'") * 100 / $(sqlite3 data/leads.db "SELECT COUNT(*) FROM emails WHERE status='sent'")" | bc
# Should be 2-5%

# Bounce rate
echo "scale=2; $(sqlite3 data/leads.db "SELECT COUNT(*) FROM emails WHERE status='bounced'") * 100 / $(sqlite3 data/leads.db "SELECT COUNT(*) FROM emails WHERE status='sent'")" | bc
# Should be <5%

# Open rate (if tracking enabled)
echo "scale=2; $(sqlite3 data/leads.db "SELECT COUNT(*) FROM emails WHERE status='opened'") * 100 / $(sqlite3 data/leads.db "SELECT COUNT(*) FROM emails WHERE status='sent'")" | bc
# Should be 15-30%
```

### Cost Analysis
```bash
# Approximate monthly cost
Posts=$(sqlite3 data/leads.db "SELECT COUNT(*) FROM raw_posts WHERE strftime('%Y-%m', created_at) = strftime('%Y-%m', 'now')")
Claude_Cost=$(echo "scale=2; $Posts * 0.003" | bc)
Gmail_Cost="6"  # Google Workspace
Total=$(echo "scale=2; $Claude_Cost + $Gmail_Cost" | bc)

echo "Monthly Cost Analysis:"
echo "Posts: $Posts"
echo "Claude API (OCR): \$$Claude_Cost"
echo "Gmail Workspace: \$$Gmail_Cost"
echo "Total: \$$Total"
```

---

## Dashboard Commands (Copy & Paste)

### All-In-One Daily Status
```bash
#!/bin/bash
echo "=== StructCrew Automation Daily Status ==="
echo
echo "Last Run:"
tail -3 logs/automation_manager.log | grep "PIPELINE"
echo
echo "Today's Status:"
cat data/automation_state.json | grep -E "posts_scraped_today|emails_sent_today"
echo
echo "Email Stats (Today):"
sqlite3 data/leads.db "SELECT COUNT(*) as sent FROM emails WHERE date(sent_at)=date('now') AND status='sent'; SELECT COUNT(*) as pending FROM emails WHERE status='pending' AND date(sent_at)=date('now')"
echo
echo "Database Size: $(du -sh data/ | cut -f1)"
```

### Weekly Email Report
```bash
#!/bin/bash
echo "=== Weekly Email Report ==="
sqlite3 data/leads.db << EOF
.mode column
SELECT 
  DATE(sent_at) as Date,
  COUNT(*) as Sent,
  SUM(CASE WHEN status='bounced' THEN 1 ELSE 0 END) as Bounced,
  SUM(CASE WHEN status='replied' THEN 1 ELSE 0 END) as Replies
FROM emails
WHERE date(sent_at) >= date('now', '-7 days')
GROUP BY DATE(sent_at)
ORDER BY date DESC;
EOF
```

### Monthly Performance
```bash
#!/bin/bash
echo "=== Monthly Performance Report ==="
echo
echo "Scraping:"
sqlite3 data/leads.db "SELECT COUNT(*) as total_posts, COUNT(DISTINCT strftime('%Y-%m-%d', created_at)) as days FROM raw_posts WHERE strftime('%Y-%m', created_at) = strftime('%Y-%m', 'now')"
echo
echo "Emails:"
sqlite3 data/leads.db "SELECT COUNT(*) as total_sent, COUNT(DISTINCT strftime('%Y-%m-%d', sent_at)) as days FROM emails WHERE status='sent' AND strftime('%Y-%m', sent_at) = strftime('%Y-%m', 'now')"
echo
echo "Engagement:"
sqlite3 data/leads.db "SELECT COUNT(*) as replies, ROUND(100.0*COUNT(*)/(SELECT COUNT(*) FROM emails WHERE status='sent' AND strftime('%Y-%m', sent_at) = strftime('%Y-%m', 'now')), 2) as response_rate FROM emails WHERE status='replied' AND strftime('%Y-%m', sent_at) = strftime('%Y-%m', 'now')"
```

---

## Alert Conditions (When to Check Deeper)

### 🔴 Critical Issues
| Condition | Action |
|-----------|--------|
| No run in 24 hours | Check Docker/container status |
| 0 emails sent | Check Gmail API quota |
| >10% bounce rate | Clean database, remove invalid emails |
| Database >50GB | Backup and archive old data |
| Instagram 403 errors | Use VPN or increase delays |

### 🟡 Warning Signs
| Condition | Action |
|-----------|--------|
| <50 emails sent/day | Check email extraction working |
| Response rate <1% | Review email template |
| 5% bounce rate | Run email validation |
| Memory usage >80% | Optimize batch sizes |
| >100 pending emails | Restart email campaign |

### 🟢 Normal Operation
- 400-500 emails sent daily
- 2-5% response rate
- <2% bounce rate
- 0 errors in logs
- Database growing ~500 rows/day

---

## Maintenance Tasks

### Weekly (10 minutes)
1. **Verify automation is running** - Check logs for errors
2. **Monitor email deliverability** - Check bounce rate
3. **Clean pending emails** - Retry stuck emails
4. **Review logs** - Look for patterns

### Monthly (30 minutes)
1. **Database maintenance** - Run integrity check
2. **Archive old data** - Backup if >50GB
3. **Update credentials** - Refresh if needed
4. **Optimize performance** - Adjust batch sizes
5. **Analyze results** - Response rates, ROI

### Quarterly (1 hour)
1. **Deep analysis** - Full database review
2. **Optimize template** - A/B test changes
3. **Review sources** - Add new scraping targets
4. **Cost optimization** - Check billing
5. **Security audit** - Update credentials

### Annually (2 hours)
1. **Full system review** - Architecture assessment
2. **Database cleanup** - Remove duplicates
3. **Cost analysis** - Yearly ROI calculation
4. **Strategy adjustment** - Plan for next year
5. **Backup plan** - Test disaster recovery

---

## Optimization Strategies

### Improve Email Deliverability
```bash
# Gradually warm up sending
# Week 1: 50 emails/day
# Week 2: 100 emails/day
# Week 3: 200 emails/day
# Week 4: 500 emails/day

# Monitor with:
sqlite3 data/leads.db "SELECT AVG(bounce_rate) FROM daily_stats WHERE week=1"
```

### Reduce OCR Costs
```bash
# Switch to Tesseract (free, lower accuracy):
# Edit .env:
USE_CLAUDE=false

# Or use Claude for tricky images only:
# Set CLAUDE_FALLBACK_THRESHOLD=0.5
```

### Speed Up Scraping
```bash
# Reduce delays (increase ban risk):
# Edit .env:
SCROLL_DELAY=1,3  # (was 3,7)

# Or use multiple accounts:
# INSTAGRAM_USERNAMES=account1,account2,account3
```

---

## Troubleshooting Guide

### Issue: Low Email Extraction Rate (<30%)
**Symptoms:** 
- Only 100-150 emails from 500 posts
- Expected: 200-300

**Causes:**
1. OCR failing on complex images
2. Email regex too strict
3. Not all posts have contact info

**Solutions:**
```bash
# Check OCR success rate
sqlite3 data/leads.db "SELECT COUNT(*) FROM extracted_text WHERE text IS NOT NULL"

# Check extraction logs
grep -i "email" logs/email_extraction.log | head -20

# Loosen email regex in extract_emails_pro.py
# Add: [a-zA-Z0-9+._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}
```

### Issue: High Bounce Rate (>5%)
**Symptoms:**
- >25 bounced emails per day

**Causes:**
1. Invalid email formats slipping through
2. Emails from test accounts
3. Typos in OCR extraction

**Solutions:**
```bash
# Verify emails before sending
# In send_campaign_pro.py, add:
result = validate_email(email)
if not result.is_valid:
    continue

# Check bounce samples
sqlite3 data/leads.db "SELECT email FROM emails WHERE status='bounced' LIMIT 20"

# Re-extract with stricter validation
# Set VALIDATE_EMAILS=true in .env
```

### Issue: Instagram Blocks Scraper
**Symptoms:**
- 403 Forbidden errors
- Scraper hangs/timeouts

**Causes:**
1. Too many requests too fast
2. Consistent user agent
3. No delays between actions

**Solutions:**
```bash
# Increase delays
SCROLL_DELAY=5,15

# Use VPN
# Install: pip install pysocks
# In scraper, add proxy configuration

# Scrape during off-peak hours
# Modify schedule:
schedule.every().day.at("23:00").do(scrape)  # 11 PM local

# Use residential proxy
# Services: Bright Data, Smartproxy, Oxylabs
```

---

## Data Backup

### Daily Backup (Automated)
```bash
# In automation_manager.py, add:
def backup_database(self):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    subprocess.run([
        'cp', 
        'data/leads.db', 
        f'data/backups/leads_{timestamp}.db'
    ])
```

### Manual Backup
```bash
# Copy entire data directory
cp -r data/ data_backup_$(date +%Y%m%d)

# Compress for storage
tar -czf data_backup.tar.gz data/

# Upload to cloud storage
# Google Drive, OneDrive, S3, etc.
```

### Restore from Backup
```bash
# Stop automation
docker stop automation

# Restore database
cp data_backup/leads.db data/leads.db

# Restart
docker start automation
```

---

## Scaling Guide

### To 1,000 Posts/Day
1. Use multiple Instagram accounts
2. Scrape different hashtags
3. Increase scraping window (use 24/7)
4. Monitor Instagram blocks

### To 1,500 Emails/Day
1. Upgrade to Google Workspace ($6/month)
2. Monitor bounce rates closely
3. Increase warm-up period
4. Consider SendGrid/Brevo alternative

### Multi-Source Scraping
1. Add LinkedIn scraper
2. Add job board scraper
3. Add company website scraper
4. Merge databases with deduplication

---

## Performance Metrics to Track

```
Daily:
- Posts scraped
- Emails extracted
- Emails sent
- Database size

Weekly:
- Total emails sent
- Response rate
- Bounce rate
- New unique addresses

Monthly:
- Cost per lead
- Response rate
- Conversion rate
- ROI
```

---

## Automation Health Check

Run this monthly:
```bash
#!/bin/bash
echo "=== System Health Check ==="
echo
echo "Container Status:"
docker ps -f "name=automation" --format "table {{.Status}}"
echo
echo "Last 10 Runs:"
grep "STARTING DAILY" logs/automation_manager.log | tail -10
echo
echo "Total Errors:"
grep "❌" logs/automation_manager.log | wc -l
echo
echo "Database Size:"
du -sh data/
echo
echo "Disk Space:"
df -h / | tail -1
echo
echo "Memory Usage:"
docker stats --no-stream --format "table {{.MemUsage}}" automation
```

---

## Support

**Monitor periodically, don't obsess.** The system handles most issues automatically.

**Key metrics to watch:**
- 1x daily: Check logs for obvious errors
- 1x weekly: Verify email counts are increasing
- 1x monthly: Analyze deliverability metrics

**Alert triggers:**
- No run in 24 hours → Restart container
- 0 emails sent → Check Gmail quota
- >10% bounce rate → Clean database

Otherwise, let it run! 🚀

---

**Remember: If it's running and emails are increasing, everything is working! ✅**
