"""
Simple SMTP Email Sender for StructCrew Campaigns
Sends personalized emails via Gmail using App Password
"""

import os
import smtplib
import sqlite3
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime
import time

# Load environment
<<<<<<< Updated upstream
=======
# Try production env first, fallback to .env
>>>>>>> Stashed changes
from pathlib import Path
if Path('.env.production').exists():
    load_dotenv('.env.production')
else:
    load_dotenv()

# Configuration
GMAIL_EMAIL = os.getenv('FROM_EMAIL', 'structcrew@gmail.com')
GMAIL_APP_PASSWORD = os.getenv('GMAIL_APP_PASSWORD', '')  # You need to set this!
FROM_NAME = os.getenv('FROM_NAME', 'StructCrew Team')
DATABASE = Path(os.getenv('DATABASE_FILE', 'data/leads.db'))
DAILY_LIMIT = int(os.getenv('DAILY_EMAIL_LIMIT', 10))

# Email template (World-Class Architectural Design)
EMAIL_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>StructCrew</title>
<style>
  /* RESET & BASE */
  body, p, h1, h2, div {{ margin: 0; padding: 0; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #F2F2F2; color: #111111; line-height: 1.6; -webkit-font-smoothing: antialiased; }}
  
  /* LAYOUT */
  .wrapper {{ width: 100%; table-layout: fixed; background-color: #F2F2F2; padding-bottom: 60px; }}
  .container {{ max-width: 600px; margin: 0 auto; background-color: #FFFFFF; }}
  
  /* HEADER */
  .header {{ padding: 60px 40px 40px; text-align: left; border-bottom: 1px solid #F0F0F0; }}
  .brand {{ font-size: 14px; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; color: #111111; margin-bottom: 20px; display: inline-block; border-bottom: 2px solid #111111; padding-bottom: 5px; }}
  .headline {{ font-size: 36px; font-weight: 800; line-height: 1.1; letter-spacing: -0.5px; color: #111111; margin-bottom: 15px; }}
  .subhead {{ font-size: 18px; color: #666666; font-weight: 400; max-width: 90%; }}

  /* CONTENT */
  .content {{ padding: 50px 40px; }}
  .pain-point {{ margin-bottom: 40px; }}
  .pain-point p {{ font-size: 18px; color: #333333; margin-bottom: 15px; }}
  .highlight {{ background: #FFF0F0; color: #D32F2F; padding: 2px 6px; border-radius: 4px; font-weight: 600; }}
  
  /* SOLUTION GRID */
  .solution-grid {{ display: table; width: 100%; margin-bottom: 50px; border-top: 1px solid #EEEEEE; padding-top: 30px; }}
  .solution-item {{ display: table-row; }}
  .check {{ display: table-cell; width: 30px; vertical-align: top; color: #111111; font-size: 20px; padding-bottom: 15px; font-weight: bold; }}
  .text {{ display: table-cell; vertical-align: top; padding-bottom: 15px; font-size: 16px; color: #555555; }}
  .text strong {{ color: #111111; }}

  /* CTA SECTION */
  .cta-section {{ background-color: #FAFAFA; padding: 50px 40px; text-align: center; border-radius: 12px; margin: 0 20px 40px; border: 1px solid #EEEEEE; }}
  .cta-title {{ font-size: 20px; font-weight: 700; margin-bottom: 25px; color: #111111; }}
  
  /* WHATSAPP BUTTON */
  .btn-whatsapp {{ background-color: #25D366; color: #FFFFFF; display: inline-block; padding: 18px 40px; border-radius: 50px; text-decoration: none; font-weight: 700; font-size: 18px; box-shadow: 0 10px 20px rgba(37, 211, 102, 0.2); transition: transform 0.2s, box-shadow 0.2s; }}
  .btn-whatsapp:hover {{ transform: translateY(-2px); box-shadow: 0 15px 30px rgba(37, 211, 102, 0.3); background-color: #22c35e; }}
  
  /* FOOTER */
  .footer {{ background-color: #111111; color: #888888; padding: 40px; text-align: center; font-size: 12px; }}
  .footer a {{ color: #FFFFFF; text-decoration: none; }}
  .footer-links {{ margin-bottom: 20px; }}
  .footer-links a {{ margin: 0 10px; text-transform: uppercase; letter-spacing: 1px; font-size: 11px; font-weight: 600; }}

  /* MOBILE */
  @media only screen and (max-width: 600px) {{
    .header {{ padding: 40px 25px; }}
    .headline {{ font-size: 30px; }}
    .content {{ padding: 40px 25px; }}
    .cta-section {{ margin: 0 0 40px; border-radius: 0; border-left: 0; border-right: 0; }}
  }}
</style>
</head>
<body>
  <div class="wrapper">
    <div class="container">
      
      <!-- HEADER -->
      <div class="header">
        <div class="brand">StructCrew</div>
        <div class="headline">Hiring shouldn't be this hard.</div>
        <div class="subhead">Hi {company}, let's fix your timeline.</div>
      </div>

      <!-- MAIN CONTENT -->
      <div class="content">
        
        <div class="pain-point">
          <p>We know the reality.</p>
          <p>Deadlines are tight. Projects are piling up. And just when you think you're set, <span class="highlight">candidates leave or don't work out.</span></p>
          <p>It's a hassle you don't need.</p>
        </div>

        <div class="solution-grid">
          <div class="solution-item">
            <div class="check">✓</div>
            <div class="text"><strong>We fix the retention problem.</strong><br>Our candidates are vetted for longevity, not just skills.</div>
          </div>
          <div class="solution-item">
            <div class="check">✓</div>
            <div class="text"><strong>We fix the timeline.</strong><br>Pre-vetted talent ready to deploy immediately.</div>
          </div>
          <div class="solution-item">
            <div class="check">✓</div>
            <div class="text"><strong>We handle the hassle.</strong><br>You interview only the top 1%. We handle the rest.</div>
          </div>
        </div>

      </div>

      <!-- CTA SECTION -->
      <div class="cta-section">
        <div class="cta-title">Let's solve this today.</div>
        <a href="https://wa.me/919312943581?text=Hi%20StructCrew,%20I'm%20interested%20in%20hiring%20architects" class="btn-whatsapp">
          Chat on WhatsApp &rarr;
        </a>
        <p style="margin-top: 20px; font-size: 14px; color: #888;">
          Or call directly: <strong>+91-9312943581</strong>
        </p>
      </div>

      <!-- FOOTER -->
      <div class="footer">
        <div class="footer-links">
          <a href="mailto:structcrew@gmail.com">EMAIL US</a>
          <a href="https://www.instagram.com/structcrew">INSTAGRAM</a>
        </div>
        <p>&copy; {current_date} StructCrew. All rights reserved.</p>
        <p style="margin-top: 10px;">
          <a href="mailto:structcrew@gmail.com?subject=Unsubscribe" style="color: #444; text-decoration: underline;">Unsubscribe</a>
        </p>
      </div>

    </div>
  </div>
</body>
</html>
"""


def send_email(to_email, company_name):
    """Send a personalized email to a lead"""
    
    if not GMAIL_APP_PASSWORD:
        print("❌ ERROR: Gmail App Password not set!")
        print("Please set GMAIL_APP_PASSWORD in your .env file")
        return False
    
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['From'] = f"{FROM_NAME} <{GMAIL_EMAIL}>"
        msg['To'] = to_email
        msg['Subject'] = f"Hiring shouldn't be this hard - {company_name}"
        
        # Personalize HTML content
        html_body = EMAIL_TEMPLATE.format(
            company=company_name,
            from_name=FROM_NAME,
            email=to_email,
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


def get_leads_to_contact(limit=None):
    """Get leads from database with status='new'"""
    
    if not DATABASE.exists():
        print(f"❌ Database not found: {DATABASE}")
        return []
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    query = "SELECT id, company, email FROM leads WHERE status='new' AND is_valid_email=1"
    
    if limit:
        query += f" LIMIT {limit}"
    
    cursor.execute(query)
    leads = cursor.fetchall()
    conn.close()
    
    return leads


def update_lead_status(lead_id, status='sent'):
    """Update lead status in database"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE leads SET status=?, sent_at=? WHERE id=?",
        (status, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), lead_id)
    )
    conn.commit()
    conn.close()


def run_campaign(test_mode=True, auto_mode=False):
    """Run the email campaign"""
    
    print("="*60)
    print("📧 StructCrew Email Campaign")
    print("="*60)
    print(f"From: {FROM_NAME} <{GMAIL_EMAIL}>")
    print(f"Daily Limit: {DAILY_LIMIT}")
    print()
    
    # Check if App Password is set
    if not GMAIL_APP_PASSWORD:
        print("⚠️  GMAIL APP PASSWORD NOT CONFIGURED!")
        print()
        print("To send emails, you need to:")
        print("1. Create a Gmail App Password: https://myaccount.google.com/apppasswords")
        print("2. Add to .env file: GMAIL_APP_PASSWORD=your-16-char-password")
        print()
        return
    
    # Get leads
    limit = 1 if test_mode else DAILY_LIMIT
    leads = get_leads_to_contact(limit)
    
    if not leads:
        print("✅ No new leads to contact!")
        print("   All leads have been contacted or no leads in database.")
        return
    
    print(f"📊 Found {len(leads)} lead(s) to contact")
    
    if test_mode:
        print("🧪 TEST MODE: Sending to 1 lead only")
    
    print()
    
    # Ask for confirmation
    if not auto_mode:
        response = input(f"Send emails to {len(leads)} lead(s)? (yes/no): ")
        
        if response.lower() not in ['yes', 'y']:
            print("❌ Campaign cancelled")
            return
    else:
        print(f"⚡ AUTO MODE: Sending to {len(leads)} lead(s) without confirmation")
    
    print()
    print("🚀 Starting campaign...")
    print()
    
    sent_count = 0
    failed_count = 0
    
    for lead_id, company, email in leads:
        success = send_email(email, company)
        
        if success:
            update_lead_status(lead_id, 'sent')
            sent_count += 1
        else:
            update_lead_status(lead_id, 'failed')
            failed_count += 1
        
        # Rate limiting (don't spam Gmail)
        time.sleep(2)
    
    print()
    print("="*60)
    print(f"✅ Campaign Complete!")
    print(f"   Sent: {sent_count}")
    print(f"   Failed: {failed_count}")
    print("="*60)


if __name__ == '__main__':
    import sys
    
    # Check command line arguments
    test_mode = '--live' not in sys.argv
    auto_mode = '--auto' in sys.argv
    
    if test_mode:
        print("🧪 Running in TEST MODE (1 email)")
        print("   To send to all leads, run: python send_emails_simple.py --live")
        print()
    
    run_campaign(test_mode=test_mode, auto_mode=auto_mode)
