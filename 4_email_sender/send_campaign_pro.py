"""
Email Campaign Sender (Gmail API)
Sends personalized cold emails with compliance and deliverability optimization
Author: StructCrew Lead Generation System
Updated: Nov 27, 2025
"""

import os
import sqlite3
import base64
import time
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import logging
from tqdm import tqdm
from datetime import datetime
import random

# Google API imports
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Setup
load_dotenv()
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/email_campaign.log'),
        logging.StreamHandler()
    ]
)

# Configuration
DB_FILE = Path(os.getenv('DATABASE_FILE', 'data/leads.db'))
CREDENTIALS_FILE = Path(os.getenv('GMAIL_CREDENTIALS', 'credentials.json'))
TOKEN_FILE = Path('data/token.json')
TEMPLATE_FILE = Path(os.getenv('EMAIL_TEMPLATE', 'templates/cold_email.html'))

# Sending limits
DAILY_LIMIT = int(os.getenv('DAILY_EMAIL_LIMIT', 100))  # Gmail free: 100/day
BATCH_SIZE = int(os.getenv('BATCH_SIZE', 50))
DELAY_BETWEEN_EMAILS = (10, 30)  # Random delay in seconds (anti-spam)

# Email configuration
FROM_NAME = os.getenv('FROM_NAME', 'Your Name')
FROM_EMAIL = os.getenv('FROM_EMAIL', 'your.email@gmail.com')
SUBJECT_TEMPLATE = os.getenv('SUBJECT', 'Architecture Collaboration Opportunity')
UNSUBSCRIBE_EMAIL = os.getenv('UNSUBSCRIBE_EMAIL', FROM_EMAIL)

# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.send']


def get_gmail_service():
    """Authenticate and return Gmail API service"""
    creds = None
    
    # Load existing credentials
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
    
    # If no valid credentials, authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CREDENTIALS_FILE.exists():
                logging.error(f"Credentials file not found: {CREDENTIALS_FILE}")
                logging.error("Download credentials.json from Google Cloud Console")
                return None
            
            flow = InstalledAppFlow.from_client_secrets_file(
                str(CREDENTIALS_FILE), SCOPES
            )
            creds = flow.run_local_server(port=0)
        
        # Save credentials
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
    
    return build('gmail', 'v1', credentials=creds)


def load_email_template():
    """Load email template from file"""
    if not TEMPLATE_FILE.exists():
        logging.warning(f"Template file not found: {TEMPLATE_FILE}")
        return None
    
    with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
        return f.read()


def personalize_email(template, lead):
    """Personalize email template with lead data"""
    # Personalization variables
    replacements = {
        '{company}': lead['company'] or 'Team',
        '{email}': lead['email'],
        '{job_title}': lead['job_title'] or 'your recent job posting',
        '{from_name}': FROM_NAME,
        '{unsubscribe_email}': UNSUBSCRIBE_EMAIL,
        '{current_date}': datetime.now().strftime('%B %d, %Y')
    }
    
    personalized = template
    for key, value in replacements.items():
        personalized = personalized.replace(key, str(value))
    
    return personalized


def create_email_message(to_email, subject, html_content):
    """Create MIME email message"""
    message = MIMEMultipart('alternative')
    message['To'] = to_email
    message['From'] = f'{FROM_NAME} <{FROM_EMAIL}>'
    message['Subject'] = subject
    
    # Add unsubscribe header (improves deliverability)
    message['List-Unsubscribe'] = f'<mailto:{UNSUBSCRIBE_EMAIL}?subject=Unsubscribe>'
    
    # Attach HTML content
    html_part = MIMEText(html_content, 'html')
    message.attach(html_part)
    
    # Encode message
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
    return {'raw': raw_message}


def send_email(service, to_email, subject, html_content):
    """Send email via Gmail API"""
    try:
        message = create_email_message(to_email, subject, html_content)
        sent_message = service.users().messages().send(
            userId='me',
            body=message
        ).execute()
        
        return True, sent_message['id']
    
    except HttpError as error:
        logging.error(f"Gmail API error: {error}")
        return False, None
    
    except Exception as e:
        logging.error(f"Unexpected error sending to {to_email}: {e}")
        return False, None


def update_lead_status(conn, lead_id, status, message_id=None, error=None):
    """Update lead status in database"""
    cursor = conn.cursor()
    
    if status == 'sent':
        cursor.execute('''
            UPDATE leads
            SET status = ?, gmail_message_id = ?, sent_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (status, message_id, lead_id))
    else:
        cursor.execute('''
            UPDATE leads
            SET status = ?, error_message = ?
            WHERE id = ?
        ''', (status, error, lead_id))
    
    conn.commit()


def add_sent_at_column():
    """Add tracking columns to database if not exists"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    try:
        cursor.execute('ALTER TABLE leads ADD COLUMN sent_at TIMESTAMP')
    except:
        pass
    
    try:
        cursor.execute('ALTER TABLE leads ADD COLUMN gmail_message_id TEXT')
    except:
        pass
    
    try:
        cursor.execute('ALTER TABLE leads ADD COLUMN error_message TEXT')
    except:
        pass
    
    conn.commit()
    conn.close()


def send_campaign(max_emails=None):
    """Main email sending function"""
    logging.info("Starting email campaign...")
    
    # Add tracking columns
    add_sent_at_column()
    
    # Load template
    template = load_email_template()
    if not template:
        logging.error("No email template found. Create one first!")
        return 0
    
    # Get Gmail service
    service = get_gmail_service()
    if not service:
        logging.error("Failed to authenticate Gmail API")
        return 0
    
    # Check quota
    try:
        profile = service.users().getProfile(userId='me').execute()
        logging.info(f"Authenticated as: {profile['emailAddress']}")
    except Exception as e:
        logging.error(f"Failed to get Gmail profile: {e}")
        return 0
    
    # Connect to database
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Get leads to send
    limit = max_emails or DAILY_LIMIT
    cursor.execute('''
        SELECT * FROM leads
        WHERE status = 'new' AND is_valid_email = 1
        ORDER BY id
        LIMIT ?
    ''', (limit,))
    
    leads = cursor.fetchall()
    total_leads = len(leads)
    
    if total_leads == 0:
        logging.warning("No new leads to send emails to")
        conn.close()
        return 0
    
    logging.info(f"Sending to {total_leads} leads (limit: {limit})")
    
    sent = 0
    failed = 0
    
    with tqdm(total=total_leads, desc="Sending emails") as pbar:
        for lead in leads:
            lead_dict = dict(lead)
            
            # Personalize email
            html_content = personalize_email(template, lead_dict)
            subject = SUBJECT_TEMPLATE.replace('{company}', lead_dict['company'] or 'Team')
            
            # Send email
            success, message_id = send_email(
                service,
                lead_dict['email'],
                subject,
                html_content
            )
            
            if success:
                update_lead_status(conn, lead_dict['id'], 'sent', message_id)
                sent += 1
                logging.info(f"✅ Sent to {lead_dict['email']} ({lead_dict['company']})")
            else:
                update_lead_status(conn, lead_dict['id'], 'failed', error='Send failed')
                failed += 1
            
            pbar.update(1)
            
            # Random delay (anti-spam)
            if sent < total_leads:
                delay = random.uniform(*DELAY_BETWEEN_EMAILS)
                time.sleep(delay)
    
    conn.close()
    
    # Summary
    logging.info(f"✅ Email Campaign Complete")
    logging.info(f"   Total Leads: {total_leads}")
    logging.info(f"   Sent: {sent}")
    logging.info(f"   Failed: {failed}")
    logging.info(f"   Success Rate: {(sent/total_leads*100):.1f}%")
    
    return sent


if __name__ == '__main__':
    print("=" * 60)
    print("📧 StructCrew Email Campaign Sender")
    print("=" * 60)
    print(f"Database: {DB_FILE}")
    print(f"Template: {TEMPLATE_FILE}")
    print(f"Daily Limit: {DAILY_LIMIT}")
    print(f"From: {FROM_NAME} <{FROM_EMAIL}>")
    print("=" * 60)
    print()
    
    result = send_campaign()
    
    print()
    print("=" * 60)
    print(f"✅ Campaign complete! Sent {result} emails")
    print("=" * 60)
