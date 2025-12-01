"""
Email & Company Extractor with NLP (SQLite Database)
Extracts emails, validates them, and stores in structured database
Author: StructCrew Lead Generation System
Updated: Nov 27, 2025
"""

import os
import re
import sqlite3
from pathlib import Path
from tqdm import tqdm
from dotenv import load_dotenv
import logging
from email_validator import validate_email, EmailNotValidError
import json

# NLP for company name extraction
try:
    import spacy
    nlp = spacy.load('en_core_web_sm')
    SPACY_AVAILABLE = True
except:
    SPACY_AVAILABLE = False
    logging.warning("spaCy not available. Install with: python -m spacy download en_core_web_sm")

# Setup
load_dotenv()
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/email_extraction.log'),
        logging.StreamHandler()
    ]
)

# Configuration
INPUT_DIR = Path(os.getenv('EXTRACTED_TEXT_DIR', 'data/extracted_text'))
DB_FILE = Path(os.getenv('DATABASE_FILE', 'data/leads.db'))
VALIDATE_EMAILS = os.getenv('VALIDATE_EMAILS', 'true').lower() == 'true'

# Ensure database directory exists
DB_FILE.parent.mkdir(parents=True, exist_ok=True)

# Regex patterns
EMAIL_REGEX = re.compile(
    r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b',
    re.IGNORECASE
)

PHONE_REGEX = re.compile(
    r'\b(?:\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b'
)

WEBSITE_REGEX = re.compile(
    r'\b(?:https?://)?(?:www\.)?[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(?:/[^\s]*)?\b',
    re.IGNORECASE
)


def init_database():
    """Initialize SQLite database with schema"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Create leads table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            website TEXT,
            job_title TEXT,
            description TEXT,
            source_file TEXT,
            instagram_post TEXT,
            is_valid_email BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'new'
        )
    ''')
    
    # Create index for faster lookups
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_email ON leads(email)
    ''')
    
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_status ON leads(status)
    ''')
    
    # Create extraction stats table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS extraction_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            total_files_processed INTEGER,
            emails_found INTEGER,
            valid_emails INTEGER,
            duplicate_emails INTEGER,
            companies_identified INTEGER,
            processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    logging.info(f"Database initialized: {DB_FILE}")


def extract_company_name(text):
    """Extract company/organization name using NLP"""
    if not SPACY_AVAILABLE:
        # Simple fallback: first line or "Unknown"
        lines = text.strip().split('\n')
        for line in lines:
            if 'Company:' in line:
                return line.split('Company:')[1].strip()
        return 'Unknown'
    
    # Use spaCy NLP
    try:
        doc = nlp(text[:500])  # Process first 500 chars for speed
        
        # Look for ORG entities
        orgs = [ent.text for ent in doc.ents if ent.label_ == 'ORG']
        if orgs:
            return orgs[0]  # Return first organization found
        
        # Fallback to "Company:" field
        if 'Company:' in text:
            match = re.search(r'Company:\s*(.+)', text, re.IGNORECASE)
            if match:
                company = match.group(1).strip()
                if company and company.lower() not in ['unknown', 'not found']:
                    return company
        
        return 'Unknown'
    
    except Exception as e:
        logging.debug(f"NLP extraction error: {e}")
        return 'Unknown'


def validate_email_address(email):
    """Validate email using email-validator"""
    if not VALIDATE_EMAILS:
        return True
    
    try:
        # Validate and get normalized form
        valid = validate_email(email, check_deliverability=False)
        return True
    except EmailNotValidError:
        return False


def extract_structured_data(text):
    """Extract all relevant data from OCR text"""
    data = {
        'company': extract_company_name(text),
        'emails': [],
        'phones': [],
        'websites': [],
        'job_title': None,
        'description': text[:500]  # First 500 chars
    }
    
    # Extract emails
    emails = EMAIL_REGEX.findall(text)
    for email in emails:
        email = email.lower().strip()
        if validate_email_address(email):
            data['emails'].append(email)
    
    # Extract phones
    phones = PHONE_REGEX.findall(text)
    data['phones'] = list(set(phones))  # Deduplicate
    
    # Extract websites
    websites = WEBSITE_REGEX.findall(text)
    data['websites'] = list(set(websites))
    
    # Extract job title (look for common patterns)
    job_title_match = re.search(r'Job Title:\s*(.+)', text, re.IGNORECASE)
    if job_title_match:
        data['job_title'] = job_title_match.group(1).strip()
    
    return data


def process_text_files():
    """Process all extracted text files"""
    logging.info("Starting email extraction...")
    
    # Initialize database
    init_database()
    
    # Get list of text files
    text_files = sorted(INPUT_DIR.glob('*.txt'))
    # Exclude metadata files
    text_files = [f for f in text_files if not f.stem.endswith('_meta')]
    
    total_files = len(text_files)
    
    if total_files == 0:
        logging.error(f"No text files found in {INPUT_DIR}")
        return 0
    
    logging.info(f"Found {total_files} text files to process")
    
    # Connect to database
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    stats = {
        'files_processed': 0,
        'emails_found': 0,
        'valid_emails': 0,
        'duplicates': 0,
        'companies_found': 0
    }
    
    with tqdm(total=total_files, desc="Extracting emails") as pbar:
        for text_file in text_files:
            try:
                # Read text
                with open(text_file, 'r', encoding='utf-8') as f:
                    text = f.read()
                
                # Extract structured data
                data = extract_structured_data(text)
                
                # Get source image name
                source_image = text_file.stem + '.jpg'
                
                # Insert each email as a separate lead
                for email in data['emails']:
                    try:
                        cursor.execute('''
                            INSERT INTO leads (
                                company, email, phone, website, 
                                job_title, description, source_file, 
                                instagram_post, is_valid_email
                            )
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (
                            data['company'],
                            email,
                            ', '.join(data['phones']) if data['phones'] else None,
                            ', '.join(data['websites']) if data['websites'] else None,
                            data['job_title'],
                            data['description'],
                            text_file.name,
                            source_image,
                            1  # is_valid_email
                        ))
                        
                        stats['emails_found'] += 1
                        stats['valid_emails'] += 1
                        
                        if data['company'] != 'Unknown':
                            stats['companies_found'] += 1
                    
                    except sqlite3.IntegrityError:
                        # Duplicate email
                        stats['duplicates'] += 1
                        logging.debug(f"Duplicate email: {email}")
                
                stats['files_processed'] += 1
            
            except Exception as e:
                logging.error(f"Error processing {text_file.name}: {e}")
            
            pbar.update(1)
    
    # Save stats to database
    cursor.execute('''
        INSERT INTO extraction_stats (
            total_files_processed, emails_found, valid_emails, 
            duplicate_emails, companies_identified
        )
        VALUES (?, ?, ?, ?, ?)
    ''', (
        stats['files_processed'],
        stats['emails_found'],
        stats['valid_emails'],
        stats['duplicates'],
        stats['companies_found']
    ))
    
    conn.commit()
    
    # Get total unique leads
    cursor.execute('SELECT COUNT(*) FROM leads')
    total_leads = cursor.fetchone()[0]
    
    conn.close()
    
    # Summary
    logging.info(f"✅ Email Extraction Complete")
    logging.info(f"   Files Processed: {stats['files_processed']}")
    logging.info(f"   Emails Found: {stats['emails_found']}")
    logging.info(f"   Valid Emails: {stats['valid_emails']}")
    logging.info(f"   Duplicates: {stats['duplicates']}")
    logging.info(f"   Companies Identified: {stats['companies_found']}")
    logging.info(f"   Total Unique Leads: {total_leads}")
    
    return total_leads


def export_to_csv():
    """Export leads to CSV for external use"""
    import pandas as pd
    
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query('SELECT * FROM leads WHERE is_valid_email = 1', conn)
    conn.close()
    
    csv_file = DB_FILE.parent / 'leads_export.csv'
    df.to_csv(csv_file, index=False)
    logging.info(f"Exported {len(df)} leads to {csv_file}")


if __name__ == '__main__':
    print("=" * 60)
    print("📧 StructCrew Email Extractor")
    print("=" * 60)
    print(f"Input: {INPUT_DIR}")
    print(f"Database: {DB_FILE}")
    print(f"Email Validation: {VALIDATE_EMAILS}")
    print(f"NLP Available: {SPACY_AVAILABLE}")
    print("=" * 60)
    print()
    
    result = process_text_files()
    
    # Export to CSV
    if result > 0:
        export_to_csv()
    
    print()
    print("=" * 60)
    print(f"✅ Extraction complete! {result} unique leads in database")
    print("=" * 60)
