# StructCrew Lead Generation - Implementation Plan

## Tomorrow's Tasks (Day 1)

### Setup (30 minutes)
1. ✅ Install Python dependencies: `pip install -r requirements.txt`
2. ✅ Create `.env` file from `.env.template`
3. ✅ Add your Instagram credentials
4. ✅ Add your Claude API key (from claude.ai)

### Testing Phase (2 hours)
1. **Test Instagram Login**
   - Run: `python 1_scraper/instagram_scraper.py`
   - Verify login works
   - Download 10 sample images

2. **Test OCR**
   - Run: `python 2_ocr/process_images.py`
   - Verify Claude can extract text
   - Check output quality

3. **Test Email Extraction**
   - Run: `python 3_email_extractor/extract_emails.py`
   - Verify emails are being found
   - Check leads.csv output

### Full Implementation (1-2 weeks)

#### Week 1: Scraping
- [ ] Scrape first 1000 posts
- [ ] Process through OCR
- [ ] Extract emails
- [ ] Review quality

#### Week 2: Email Campaign
- [ ] Set up Gmail API
- [ ] Test email template with 10 leads
- [ ] Review responses
- [ ] Scale to 500/day

## Important Notes

### Rate Limiting
- Instagram: Max 100-200 posts/hour (use delays)
- Claude API: Check your plan limits
- Gmail: 500 emails/day max

### Cost Estimates
- Claude API: ~$0.003 per image (20k images = $60)
- Gmail API: Free
- Time: 10-20 hours of automated processing

### Legal Compliance
Before sending emails:
1. Add physical address to template
2. Test unsubscribe mechanism
3. Keep track of unsubscribe requests
4. Include clear opt-out in every email

## Expected Results

- **Scraping Success Rate**: 80-90% (some posts may fail)
- **Email Extraction Rate**: 40-60% (not all posts have emails)
- **Expected Leads**: 8,000-12,000 unique emails
- **Email Response Rate**: 2-5% (industry standard for cold emails)
- **Expected Clients**: 160-600 interested leads

## Troubleshooting

### If Instagram blocks you:
- Use longer delays (5-10 seconds between actions)
- Scrape during off-peak hours
- Consider using proxy/VPN

### If OCR quality is poor:
- Switch to Tesseract OCR (free, but lower quality)
- Manually review first 100 results
- Adjust Claude prompt

### If emails bounce:
- Use email verification service (Hunter.io has free tier)
- Remove bounced emails from list
- Check spam score of your template

---

**Ready to start tomorrow!** 🚀
