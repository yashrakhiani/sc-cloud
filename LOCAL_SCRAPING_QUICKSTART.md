# 🚀 Local Multi-PC Scraping - Quick Start

**Setup time:** 5 minutes per PC  
**Posts per PC per day:** 500  
**Database growth:** Unlimited (all synced to GitHub)

---

## One-Command Setup

```bash
git clone https://github.com/yashrakhiani/sc-cloud.git
cd sc-cloud
python setup_multi_pc.py
```

Answer one question: **What's your PC name?** (e.g., "home-pc-1")

That's it! The scraper will:
- ✅ Install dependencies
- ✅ Setup auto-scheduling
- ✅ Start scraping 500 posts/day
- ✅ Auto-sync to GitHub

---

## What Happens Automatically

```
Your Computer (Every Day)
├─ 00:00 → Scrape 100 posts
├─ 04:00 → Scrape 100 posts
├─ 08:00 → Scrape 100 posts
├─ 12:00 → Scrape 100 posts
├─ 16:00 → Scrape 100 posts
└─ Auto-push to GitHub after each session
     ↓
Shared Database on GitHub
     ↓
500 posts daily growing database
```

---

## Multi-PC Setup (Scale It Up)

Want more posts? Add more computers.

### On PC #1 (Home):
```bash
python setup_multi_pc.py
# Name: home-pc-1
```

### On PC #2 (Office):
```bash
python setup_multi_pc.py
# Name: office-pc-2
```

### On PC #3 (Laptop):
```bash
python setup_multi_pc.py
# Name: laptop-pc-3
```

**Result:**
```
PC #1: 500 posts/day
PC #2: 500 posts/day
PC #3: 500 posts/day
────────────────────
Total: 1,500 posts/day
All deduplicated ✓
```

---

## Monitor Progress

### Real-Time Logs
```bash
tail -f logs/local_scraper.log
```

### GitHub Activity
```bash
git log --oneline | head -10
```

### Database Growth
```bash
sqlite3 data/leads.db "SELECT COUNT(*) FROM raw_posts"
```

---

## Expected Results

**After 24 hours (1 PC):**
- 500 posts downloaded
- ~200-300 emails extracted
- Ready for email campaign

**After 1 week (3 PCs):**
- 10,000+ posts
- 4,000-6,000 emails
- Growing exponentially

**After 1 month (3 PCs):**
- 45,000+ posts
- 18,000-27,000 emails
- Database worth $10K+ in leads

---

## That's All!

Scraping runs automatically. Your database grows daily. Add more PCs anytime.

---

**Questions?** See `MULTI_PC_LOCAL_SETUP.md` for full documentation.
