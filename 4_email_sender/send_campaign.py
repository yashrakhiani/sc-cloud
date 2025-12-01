"""
Email Campaign Sender
Sends personalized cold emails to extracted leads using Gmail API
"""

import os
import pandas as pd
import time
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import base64
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from dotenv import load_dotenv
import logging

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('../logs/sender.log'),
        logging.StreamHandler()
    ]
)

class EmailCampaign:
    def __init__(self):
        self.leads_csv = pd.read_csv('../data/leads.csv')
        self.sent_csv_path = '../data/sent_emails.csv'
        self.daily_limit = int(os.getenv('DAILY_EMAIL_LIMIT', 500))
        self.sender_email = os.getenv('SENDER_EMAIL')
        self.sender_name = os.getenv('SENDER_NAME')
        
        # Load Gmail credentials (you'll need to set this up)
        # self.gmail_service = self.setup_gmail()
        
    def load_template(self, template_name='default'):
        """Load email template"""
        template_path = f'../templates/{template_name}.txt'
        with open(template_path, 'r') as f:
            return f.read()
    
    def personalize_email(self, template, company_name):
        """Personalize email template with company name"""
        return template.replace('{{COMPANY_NAME}}', company_name)
    
    def send_email(self, to_email, subject, body):
        """Send email using Gmail API"""
        # TODO: Implement Gmail API sending
        # This is a placeholder
        logging.info(f"Sending email to {to_email}")
        time.sleep(0.1)  # Simulate sending delay
        return True
    
    def run_campaign(self):
        """Send emails to all leads"""
        # Filter leads that haven't been contacted
        pending = self.leads_csv[self.leads_csv['Status'] == 'Not Contacted']
        
        logging.info(f"Found {len(pending)} leads to contact")
        
        template = self.load_template()
        sent_today = 0
        
        for idx, lead in pending.iterrows():
            if sent_today >= self.daily_limit:
                logging.info(f"Daily limit of {self.daily_limit} reached. Stopping for today.")
                break
            
            try:
                personalized_body = self.personalize_email(template, lead['Company'])
                success = self.send_email(
                    lead['Email'],
                    "Affordable Recruitment Solutions for Architecture Studios",
                    personalized_body
                )
                
                if success:
                    # Update status
                    self.leads_csv.at[idx, 'Status'] = 'Sent'
                    self.leads_csv.at[idx, 'Sent_Date'] = datetime.now().strftime('%Y-%m-%d')
                    sent_today += 1
                    
            except Exception as e:
                logging.error(f"Failed to send to {lead['Email']}: {e}")
        
        # Save updated leads CSV
        self.leads_csv.to_csv(self.sent_csv_path, index=False)
        logging.info(f"Campaign complete. Sent {sent_today} emails today.")

if __name__ == "__main__":
    campaign = EmailCampaign()
    campaign.run_campaign()
