"""
Follow-Up Campaign Manager
Sends follow-up emails to leads after 15 or 30 days
Author: StructCrew Lead Generation System
"""

import os
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime, timedelta
import time
import sys

# Load environment
load_dotenv()

# Configuration
GMAIL_EMAIL = os.getenv('FROM_EMAIL', 'structcrew@gmail.com')
GMAIL_APP_PASSWORD = os.getenv('GMAIL_APP_PASSWORD', '')
FROM_NAME = os.getenv('FROM_NAME', 'StructCrew Team')
DATABASE = Path(os.getenv('DATABASE_FILE', 'data/leads.db'))

# Follow-up templates
FOLLOWUP_15_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background-color: #F2F2F2; color: #111111; line-height: 1.6; }}
  .container {{ max-width: 600px; margin: 0 auto; background-color: #FFFFFF; padding: 40px; }}
  .header {{ margin-bottom: 30px; }}
  .brand {{ font-size: 14px; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; color: #111111; margin-bottom: 20px; }}
  .headline {{ font-size: 32px; font-weight: 800; line-height: 1.2; color: #111111; margin-bottom: 15px; }}
  .content {{ font-size: 16px; color: #333333; margin-bottom: 30px; }}
  .highlight {{ background: #FFF8E1; color: #F57C00; padding: 2px 6px; border-radius: 4px; font-weight: 600; }}
  .btn-whatsapp {{ background-color: #25D366; color: #FFFFFF; display: inline-block; padding: 16px 35px; border-radius: 50px; text-decoration: none; font-weight: 700; font-size: 16px; margin: 20px 0; }}
  .footer {{ margin-top: 40px; padding-top: 20px; border-top: 1px solid #EEEEEE; font-size: 12px; color: #888888; text-align: center; }}
</style>
</head>
<body>
  <div class="container">
    <div class="header">
      <div class="brand">StructCrew</div>
      <div class="headline">Still struggling with hiring?</div>
    </div>
    
    <div class="content">
      <p>Hi {company},</p>
      
      <p>I reached out a couple weeks ago about your hiring needs.</p>
      
      <p>I know finding the right architects is <span class="highlight">time-consuming and frustrating</span>.</p>
      
      <p>That's exactly why we built StructCrew:</p>
      
      <ul style="margin: 20px 0;">
        <li style="margin-bottom: 10px;">✓ Pre-vetted candidates ready to start</li>
        <li style="margin-bottom: 10px;">✓ 90% retention rate (they actually stay)</li>
        <li style="margin-bottom: 10px;">✓ Fill positions in days, not months</li>
      </ul>
      
      <p>If you're still looking, let's talk.</p>
      
      <a href="https://wa.me/919312943581?text=Hi%20StructCrew,%20I'm%20interested%20in%20hiring" class="btn-whatsapp">
        Quick Chat on WhatsApp →
      </a>
      
      <p style="margin-top: 20px; font-size: 14px; color: #666;">
        Or call: <strong>+91-9312943581</strong>
      </p>
    </div>
    
    <div class="footer">
      <p>© {current_date} StructCrew. All rights reserved.</p>
      <p style="margin-top: 10px;">
        <a href="mailto:structcrew@gmail.com?subject=Unsubscribe" style="color: #444; text-decoration: underline;">Unsubscribe</a>
      </p>
    </div>
  </div>
</body>
</html>
"""

FOLLOWUP_30_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background-color: #F2F2F2; color: #111111; line-height: 1.6; }}
  .container {{ max-width: 600px; margin: 0 auto; background-color: #FFFFFF; padding: 40px; }}
  .header {{ margin-bottom: 30px; }}
  .brand {{ font-size: 14px; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; color: #111111; margin-bottom: 20px; }}
  .headline {{ font-size: 32px; font-weight: 800; line-height: 1.2; color: #111111; margin-bottom: 15px; }}
  .content {{ font-size: 16px; color: #333333; margin-bottom: 30px; }}
  .highlight {{ background: #FFEBEE; color: #C62828; padding: 2px 6px; border-radius: 4px; font-weight: 600; }}
  .btn-whatsapp {{ background-color: #25D366; color: #FFFFFF; display: inline-block; padding: 16px 35px; border-radius: 50px; text-decoration: none; font-weight: 700; font-size: 16px; margin: 20px 0; }}
  .footer {{ margin-top: 40px; padding-top: 20px; border-top: 1px solid #EEEEEE; font-size: 12px; color: #888888; text-align: center; }}
</style>
</head>
<body>
  <div class="container">
    <div class="header">
      <div class="brand">StructCrew</div>
      <div class="headline">Last chance to connect</div>
    </div>
    
    <div class="content">
      <p>Hi {company},</p>
      
      <p>This is my final email.</p>
      
      <p>I've reached out twice about helping you hire architects faster.</p>
      
      <p>If you're <span class="highlight">still hiring</span> or think you might need help in the future, let's connect now.</p>
      
      <p><strong>What we offer:</strong></p>
      
      <ul style="margin: 20px 0;">
        <li style="margin-bottom: 10px;">✓ Vetted talent pool ready to deploy</li>
        <li style="margin-bottom: 10px;">✓ Replace candidates who leave (free)</li>
        <li style="margin-bottom: 10px;">✓ Fill positions in 7 days or less</li>
      </ul>
      
      <p>One quick chat could save you months of hiring headaches.</p>
      
      <a href="https://wa.me/919312943581?text=Hi%20StructCrew,%20let's%20talk%20about%20hiring" class="btn-whatsapp">
        Let's Talk on WhatsApp →
      </a>
      
      <p style="margin-top: 20px; font-size: 14px; color: #666;">
        Or call: <strong>+91-9312943581</strong>
      </p>
      
      <p style="margin-top: 30px; font-size: 14px; color: #888;">
        If I don't hear from you, I'll assume you're all set. Best of luck with your projects! 🏗️
      </p>
    </div>
    
    <div class="footer">
      <p>© {current_date} StructCrew. All rights reserved.</p>
      <p style="margin-top: 10px;">
        <a href="mailto:structcrew@gmail.com?subject=Unsubscribe" style="color: #444; text-decoration: underline;">Unsubscribe</a>
      </p>
    </div>
  </div>
</body>
</html>
"""


def send_followup_email(to_email, company_name, template, subject):
    """Send a follow-up email"""
    
    if not GMAIL_APP_PASSWORD:
        print("❌ ERROR: Gmail App Password not set!")
        return False
    
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['From'] = f"{FROM_NAME} <{GMAIL_EMAIL}>"
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # Personalize HTML content
        html_body = template.format(
            company=company_name,
            current_date=datetime.now().strftime('%B %d, %Y')
        )
        
        # Attach HTML
        html_part = MIMEText(html_body, 'html')
        msg.attach(html_part)
        
        # Send via Gmail SMTP
        print(f"📧 Sending to {company_name} ({to_email})...")
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(GMAIL_EMAIL, GMAIL_APP_PASSWORD)
            server.send_message(msg)
        
        print(f"   ✅ Sent successfully!")
        return True
        
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        return False


def get_followup_leads(days_ago, status='sent'):
    """Get leads ready for follow-up"""
    
    if not DATABASE.exists():
        print(f"❌ Database not found: {DATABASE}")
        return []
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Calculate cutoff date
    cutoff_date = (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d')
    
    query = """
        SELECT id, company, email, sent_at 
        FROM leads 
        WHERE status = ? 
        AND DATE(sent_at) <= ? 
        AND is_valid_email = 1
    """
    
    cursor.execute(query, (status, cutoff_date))
    leads = cursor.fetchall()
    conn.close()
    
    return leads


def update_followup_status(lead_id, status):
    """Update lead status after follow-up"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE leads SET status=?, sent_at=? WHERE id=?",
        (status, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), lead_id)
    )
    conn.commit()
    conn.close()


def run_followup_campaign(days=15, dry_run=False):
    """Run follow-up campaign"""
    
    print("=" * 60)
    print(f"📧 StructCrew Follow-Up Campaign ({days} days)")
    print("=" * 60)
    print(f"From: {FROM_NAME} <{GMAIL_EMAIL}>")
    print(f"Looking for leads sent {days}+ days ago")
    print()
    
    # Get leads
    leads = get_followup_leads(days)
    
    if not leads:
        print(f"✅ No leads ready for {days}-day follow-up!")
        return
    
    print(f"📊 Found {len(leads)} lead(s) ready for follow-up")
    print()
    
    # Choose template and status
    if days == 15:
        template = FOLLOWUP_15_TEMPLATE
        subject = "Still looking for architects?"
        new_status = 'followup_15'
    elif days == 30:
        template = FOLLOWUP_30_TEMPLATE
        subject = "Last chance to connect - StructCrew"
        new_status = 'followup_30'
    else:
        print("❌ Invalid days. Use 15 or 30.")
        return
    
    if dry_run:
        print("🧪 DRY RUN MODE - No emails will be sent")
        print()
        for lead_id, company, email, sent_at in leads:
            print(f"Would send to: {company} ({email}) - Originally sent: {sent_at}")
        return
    
    # Ask for confirmation
    response = input(f"Send {days}-day follow-up to {len(leads)} lead(s)? (yes/no): ")
    
    if response.lower() not in ['yes', 'y']:
        print("❌ Campaign cancelled")
        return
    
    print()
    print("🚀 Starting follow-up campaign...")
    print()
    
    sent_count = 0
    failed_count = 0
    
    for lead_id, company, email, sent_at in leads:
        success = send_followup_email(email, company, template, subject)
        
        if success:
            update_followup_status(lead_id, new_status)
            sent_count += 1
        else:
            failed_count += 1
        
        # Rate limiting
        time.sleep(2)
    
    print()
    print("=" * 60)
    print(f"✅ Follow-Up Campaign Complete!")
    print(f"   Sent: {sent_count}")
    print(f"   Failed: {failed_count}")
    print("=" * 60)


if __name__ == '__main__':
    # Parse command line arguments
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python followup_campaign.py 15          # Send 15-day follow-up")
        print("  python followup_campaign.py 30          # Send 30-day follow-up")
        print("  python followup_campaign.py 15 --dry-run  # Test without sending")
        sys.exit(1)
    
    days = int(sys.argv[1])
    dry_run = '--dry-run' in sys.argv
    
    run_followup_campaign(days=days, dry_run=dry_run)
