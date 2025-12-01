"""
Email Extractor
Parses OCR text files and extracts emails, company names, and other contact info
"""

import re
import pandas as pd
from pathlib import Path
import logging
from tqdm import tqdm

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('../logs/extractor.log'),
        logging.StreamHandler()
    ]
)

class EmailExtractor:
    def __init__(self):
        self.text_dir = Path('../data/extracted_text')
        self.output_csv = Path('../data/leads.csv')
        
        # Email regex pattern
        self.email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        
        # Phone regex pattern (Indian format)
        self.phone_pattern = r'(\+91[\-\s]?)?[6789]\d{9}'
        
        # Website pattern
        self.website_pattern = r'(https?://)?([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}'
        
    def extract_from_text(self, text):
        """Extract contact information from text"""
        emails = re.findall(self.email_pattern, text)
        phones = re.findall(self.phone_pattern, text)
        websites = re.findall(self.website_pattern, text)
        
        # Try to extract company name (usually in first few lines)
        lines = text.split('\n')
        company_name = lines[0] if lines else "Unknown"
        
        return {
            'emails': list(set(emails)),  # Remove duplicates
            'phones': list(set([p[1] if isinstance(p, tuple) else p for p in phones])),
            'websites': list(set([w[0] + w[1] for w in websites if isinstance(w, tuple)])),
            'company_name': company_name
        }
    
    def process_all_texts(self):
        """Process all extracted text files"""
        text_files = list(self.text_dir.glob('*.txt'))
        logging.info(f"Found {len(text_files)} text files to process")
        
        leads_data = []
        
        for text_file in tqdm(text_files, desc="Extracting emails"):
            with open(text_file, 'r', encoding='utf-8') as f:
                text = f.read()
                
            extracted = self.extract_from_text(text)
            
            # Create a row for each email found
            for email in extracted['emails']:
                leads_data.append({
                    'Company': extracted['company_name'],
                    'Email': email,
                    'Phone': ', '.join(extracted['phones']),
                    'Website': ', '.join(extracted['websites']),
                    'Source': text_file.name,
                    'Status': 'Not Contacted'
                })
        
        # Create DataFrame and save
        df = pd.DataFrame(leads_data)
        df = df.drop_duplicates(subset=['Email'])  # Remove duplicate emails
        df.to_csv(self.output_csv, index=False)
        
        logging.info(f"Extracted {len(df)} unique leads")
        logging.info(f"Saved to {self.output_csv}")
        
        return df

if __name__ == "__main__":
    extractor = EmailExtractor()
    leads_df = extractor.process_all_texts()
    print(leads_df.head())
