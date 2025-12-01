# ✅ Email Campaign Compliance Checklist

## Before You Send ANY Emails

This checklist ensures you comply with CAN-SPAM (US), GDPR (EU), and CASL (Canada) regulations.

---

## 🔴 CRITICAL - Must Complete Before Sending

### 1. Business Identity
- [ ] Your **real name** or business name is in the email template
- [ ] **Valid physical address** added to email footer (required by CAN-SPAM)
  - Can be: Office address, PO Box, or registered agent address
  - Update in `templates/cold_email.html`

### 2. Unsubscribe Mechanism
- [ ] "Unsubscribe" link or instructions in EVERY email
- [ ] Unsubscribe email address is monitored daily
- [ ] Can process unsubscribe requests within **10 business days** (CAN-SPAM)
- [ ] Database tracks unsubscribed emails to prevent re-sending
- [ ] List-Unsubscribe header included (automated in scripts)

### 3. Email Content
- [ ] Subject line **accurately reflects** email content (not misleading)
- [ ] Email clearly identifies it's an **advertisement/solicitation**
- [ ] No deceptive headers (From, Reply-To are accurate)
- [ ] No false or misleading sender information

### 4. Technical Setup
- [ ] Gmail account ready and verified
- [ ] SPF record set up (for custom domain) - Optional but recommended
- [ ] DKIM signature enabled (for custom domain) - Optional but recommended
- [ ] DMARC policy configured (for custom domain) - Optional but recommended
- [ ] Reply-to email monitored daily

---

## 🟡 RECOMMENDED - Improve Deliverability & Compliance

### 5. Legitimate Interest (GDPR)
- [ ] You have **legitimate interest** to contact these businesses
  - ✅ They posted public job openings
  - ✅ You offer relevant recruitment services
  - ✅ Business-to-business (B2B) relationship
- [ ] Document your reasoning for why each lead is relevant
- [ ] Be prepared to explain if challenged

### 6. Data Protection
- [ ] Leads database stored **securely** (not public)
- [ ] `.env` file with credentials is **not committed to Git**
- [ ] Instagram cookies file is **private**
- [ ] Access to database limited to authorized users only
- [ ] Have a plan to delete data if requested (GDPR Right to Erasure)

### 7. Opt-out Tracking
- [ ] Create "unsubscribe list" database table or file
- [ ] Cross-reference every send against unsubscribe list
- [ ] Never re-add someone who unsubscribed
- [ ] Keep unsubscribe records for **minimum 3 years**

### 8. Transparency
- [ ] Privacy Policy available (link in email footer)
  - Explain what data you collect
  - How you got their email
  - How data is used
  - How to opt out
  - How long data is retained
- [ ] Create simple page on your website: `yoursite.com/privacy`

---

## 🟢 BEST PRACTICES - Professional Standards

### 9. Email Quality
- [ ] Test email template on multiple devices (desktop, mobile)
- [ ] Check spam score before sending: [Mail-tester.com](https://www.mail-tester.com/)
- [ ] Send test emails to yourself first
- [ ] Proofread for typos and grammar
- [ ] Verify all links work (Calendar, website, social media)

### 10. Sender Reputation
- [ ] **Warm up** email address gradually:
  - Week 1: 20-50 emails/day
  - Week 2: 100 emails/day
  - Week 3+: Full volume
- [ ] Monitor bounce rate (keep below 5%)
- [ ] Monitor spam complaints (keep below 0.1%)
- [ ] Don't buy email lists (use only scraped/organic leads)

### 11. Personalization & Relevance
- [ ] Email is personalized (not generic blast)
- [ ] Company name included
- [ ] Reference to their specific job post
- [ ] Clear value proposition (what's in it for them?)
- [ ] Professional tone and design

### 12. Response Management
- [ ] Monitor reply inbox **daily**
- [ ] Respond to inquiries within **24 hours**
- [ ] Respond to complaints professionally
- [ ] Honor unsubscribe requests **immediately**
- [ ] Track responses in CRM/spreadsheet

---

## 📊 Pre-Launch Testing

### Test Campaign (10 emails)
- [ ] Send to 10 test leads (or your own email addresses)
- [ ] Verify template renders correctly
- [ ] Check all links work
- [ ] Confirm unsubscribe link functions
- [ ] Monitor for bounces
- [ ] Wait 24 hours and review results

### Pilot Campaign (50-100 emails)
- [ ] Send to 50-100 real leads
- [ ] Monitor deliverability (inbox vs spam folder)
- [ ] Track open rates (expect 20-30%)
- [ ] Track response rate (expect 2-5%)
- [ ] Review spam complaints (should be 0%)
- [ ] Adjust template if needed

---

## 🚨 During Campaign - Daily Checks

### Daily Monitoring (5 minutes/day)
- [ ] Check bounce rate
- [ ] Check spam complaints
- [ ] Process unsubscribe requests
- [ ] Respond to replies
- [ ] Verify daily sending limit not exceeded
- [ ] Review any delivery errors in logs

### Weekly Review (30 minutes/week)
- [ ] Calculate response rate
- [ ] Update database with bounce/invalid emails
- [ ] Review email performance (opens, clicks)
- [ ] Adjust template if performance is poor
- [ ] Document any compliance issues

---

## 🛑 Red Flags - Stop Immediately If:

1. **Bounce rate > 10%**: Your list quality is poor
2. **Spam complaints > 0.5%**: Your content is problematic
3. **Gmail/SMTP blocks your account**: You're flagged as spammer
4. **Legal complaint received**: Contact lawyer IMMEDIATELY
5. **Deliverability < 70%**: Fix technical issues before continuing

---

## 📝 Documentation to Keep

### Maintain Records Of:
1. **Consent/Source:** Where each email came from (Instagram @archijobs)
2. **Send logs:** Who was emailed, when, with what content
3. **Unsubscribe requests:** Date, email address, action taken
4. **Bounce/complaint logs:** Failed sends, reasons
5. **Response tracking:** Replies received, follow-up actions

**Retention period:** Minimum 3 years (GDPR/CASL requirement)

---

## ⚖️ Legal Disclaimers

### Add to Your Email Footer:
```html
<p style="font-size: 12px; color: #666;">
  You received this email because you posted a job opening on Instagram (@archijobs). 
  We believe our recruitment services could benefit your studio. 
  If you do not wish to receive future emails, please reply with "UNSUBSCRIBE" 
  or click the unsubscribe link above.
</p>

<p style="font-size: 11px; color: #999;">
  [Your Business Name]<br>
  [Your Physical Address]<br>
  [City, State, ZIP]
</p>
```

---

## 🌍 International Compliance

### Sending to EU Recipients (GDPR)
- [ ] Document legitimate interest
- [ ] Make opt-out easy and prominent
- [ ] Process opt-outs within 30 days
- [ ] Provide data access if requested
- [ ] Delete data if requested (Right to Erasure)

### Sending to Canada (CASL)
- [ ] Existing business relationship OR express consent
- [ ] Clear identification of sender
- [ ] Unsubscribe mechanism free of charge
- [ ] Process opt-outs within 10 business days

### Sending to Australia (Spam Act 2003)
- [ ] Consent or existing relationship
- [ ] Accurate sender info
- [ ] Functional unsubscribe within 5 days

---

## ✅ Final Sign-Off

**I confirm that I have:**
- [ ] Read and understand CAN-SPAM, GDPR, and CASL requirements
- [ ] Completed ALL critical checklist items (Section 1-4)
- [ ] Added my business address to email template
- [ ] Set up unsubscribe monitoring
- [ ] Tested emails on myself first
- [ ] Have a plan to handle unsubscribe requests daily
- [ ] Will monitor metrics and stop if red flags appear
- [ ] Understand this is B2B outreach (not B2C spam)

**Date:** ________________  
**Signature:** ________________

---

## 📚 Reference Links

- [CAN-SPAM Compliance Guide](https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business)
- [GDPR Official Text](https://gdpr.eu/)
- [CASL Guide](https://crtc.gc.ca/eng/casl-lcap.htm)
- [Email Deliverability Best Practices](https://www.validity.com/resource-center/email-deliverability-best-practices/)

---

**Remember: When in doubt, DON'T send. Consult a lawyer if unsure about any compliance issue.**
