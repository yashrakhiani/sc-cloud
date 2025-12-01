"""
OCR Text Extraction (Claude Vision API + Tesseract Fallback)
Extracts text from Instagram job post images
Author: StructCrew Lead Generation System
Updated: Nov 27, 2025
"""

import os
import base64
import json
from pathlib import Path
from tqdm import tqdm
from dotenv import load_dotenv
import logging
from anthropic import Anthropic
import time

# Tesseract fallback
try:
    import pytesseract
    from PIL import Image
    TESSERACT_AVAILABLE = True
    
    # Set Tesseract path based on OS
    if os.name == 'nt':  # Windows
        tesseract_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        if os.path.exists(tesseract_path):
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
    # On Linux (Docker/Cloud), it's usually in the PATH automatically
    
except ImportError:
    TESSERACT_AVAILABLE = False
    logging.warning("Tesseract not available. Install pytesseract and Tesseract binary for fallback OCR.")

# Setup
load_dotenv()
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/ocr.log'),
        logging.StreamHandler()
    ]
)

# Configuration
INPUT_DIR = Path(os.getenv('RAW_IMAGES_DIR', 'data/raw_images'))
OUTPUT_DIR = Path(os.getenv('EXTRACTED_TEXT_DIR', 'data/extracted_text'))
CLAUDE_API_KEY = os.getenv('CLAUDE_API_KEY')
USE_CLAUDE = os.getenv('USE_CLAUDE', 'true').lower() == 'true'
BATCH_SIZE = int(os.getenv('OCR_BATCH_SIZE', 50))  # Process in batches
RATE_LIMIT_DELAY = 1  # Delay between API calls (seconds)

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Claude prompt optimized for job posts
CLAUDE_PROMPT = """Extract ALL text from this job posting image. Focus on:
1. Company/Studio name
2. Email addresses
3. Contact information (phone, website)
4. Job title and description
5. Any other visible text

Output in this structured format:
---
Company: [company name if found, else "Unknown"]
Email: [email addresses, comma-separated if multiple]
Phone: [phone numbers if found]
Website: [website if found]
Job Title: [job title if found]
Description: [brief job description or other relevant text]
Source: [any social media handles or additional contact info]
---

If any field is not found, write "Not found". Be thorough and extract ALL visible text."""


def encode_image(image_path):
    """Encode image to base64"""
    with open(image_path, 'rb') as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')


def extract_text_claude(image_path, client):
    """Extract text using Claude Vision API"""
    try:
        img_data = encode_image(image_path)
        
        message = client.messages.create(
            model='claude-3-haiku-20240307',  # Haiku for speed & cost efficiency
            max_tokens=1024,
            messages=[
                {
                    'role': 'user',
                    'content': [
                        {
                            'type': 'image',
                            'source': {
                                'type': 'base64',
                                'media_type': 'image/jpeg',
                                'data': img_data
                            }
                        },
                        {
                            'type': 'text',
                            'text': CLAUDE_PROMPT
                        }
                    ]
                }
            ]
        )
        
        extracted_text = message.content[0].text
        return extracted_text, 'claude'
    
    except Exception as e:
        logging.error(f"Claude API error for {image_path.name}: {e}")
        return None, 'error'


def extract_text_tesseract(image_path):
    """Extract text using Tesseract OCR (fallback)"""
    if not TESSERACT_AVAILABLE:
        return "Tesseract not installed", 'unavailable'
    
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        return text, 'tesseract'
    
    except Exception as e:
        logging.error(f"Tesseract error for {image_path.name}: {e}")
        return None, 'error'


def process_images():
    """Main OCR processing function"""
    logging.info("Starting OCR processing...")
    
    # Get list of images
    image_files = sorted(INPUT_DIR.glob('*.jpg'))
    total_images = len(image_files)
    
    if total_images == 0:
        logging.error(f"No images found in {INPUT_DIR}")
        return 0
    
    logging.info(f"Found {total_images} images to process")
    
    # Initialize Claude client
    client = None
    if USE_CLAUDE and CLAUDE_API_KEY:
        client = Anthropic(api_key=CLAUDE_API_KEY)
        logging.info("Using Claude Vision API for OCR")
    else:
        logging.info("Using Tesseract for OCR (fallback mode)")
    
    processed = 0
    errors = 0
    
    # Statistics
    stats = {
        'total': total_images,
        'claude_success': 0,
        'tesseract_success': 0,
        'errors': 0,
        'skipped': 0
    }
    
    with tqdm(total=total_images, desc="Processing images") as pbar:
        for image_file in image_files:
            # Check if already processed
            output_file = OUTPUT_DIR / f"{image_file.stem}.txt"
            metadata_file = OUTPUT_DIR / f"{image_file.stem}_meta.json"
            
            if output_file.exists():
                logging.debug(f"Skipping {image_file.name} (already processed)")
                stats['skipped'] += 1
                pbar.update(1)
                continue
            
            # Try Claude first, fallback to Tesseract
            extracted_text = None
            method = None
            
            if client:
                extracted_text, method = extract_text_claude(image_file, client)
                time.sleep(RATE_LIMIT_DELAY)  # Rate limiting
            
            # Fallback to Tesseract if Claude fails
            if not extracted_text and TESSERACT_AVAILABLE:
                logging.info(f"Falling back to Tesseract for {image_file.name}")
                extracted_text, method = extract_text_tesseract(image_file)
            
            if extracted_text:
                # Save extracted text
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(extracted_text)
                
                # Save metadata
                metadata = {
                    'image_file': image_file.name,
                    'method': method,
                    'processed_at': time.strftime('%Y-%m-%d %H:%M:%S'),
                    'text_length': len(extracted_text)
                }
                
                with open(metadata_file, 'w') as f:
                    json.dump(metadata, f, indent=2)
                
                processed += 1
                
                if method == 'claude':
                    stats['claude_success'] += 1
                elif method == 'tesseract':
                    stats['tesseract_success'] += 1
                
                logging.debug(f"Processed: {image_file.name} ({method})")
            
            else:
                errors += 1
                stats['errors'] += 1
                logging.error(f"Failed to extract text from {image_file.name}")
            
            pbar.update(1)
    
    # Summary
    logging.info(f"✅ OCR Processing Complete")
    logging.info(f"   Total: {total_images}")
    logging.info(f"   Processed: {processed}")
    logging.info(f"   Claude: {stats['claude_success']}")
    logging.info(f"   Tesseract: {stats['tesseract_success']}")
    logging.info(f"   Skipped: {stats['skipped']}")
    logging.info(f"   Errors: {errors}")
    
    # Save stats
    stats_file = OUTPUT_DIR / 'processing_stats.json'
    with open(stats_file, 'w') as f:
        json.dump(stats, f, indent=2)
    
    return processed


if __name__ == '__main__':
    print("=" * 60)
    print("🔍 StructCrew OCR Text Extractor")
    print("=" * 60)
    print(f"Input: {INPUT_DIR}")
    print(f"Output: {OUTPUT_DIR}")
    print(f"Method: {'Claude Vision API' if USE_CLAUDE and CLAUDE_API_KEY else 'Tesseract OCR'}")
    print("=" * 60)
    print()
    
    result = process_images()
    
    print()
    print("=" * 60)
    print(f"✅ Processing complete! Extracted text from {result} images")
    print("=" * 60)
