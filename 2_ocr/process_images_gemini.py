"""
OCR Text Extraction using Google Gemini Vision API
Extracts text from Instagram job post images
Author: StructCrew Lead Generation System
Updated: Nov 28, 2025
"""

import os
import base64
import json
from pathlib import Path
from tqdm import tqdm
from dotenv import load_dotenv
import logging
import time
import requests

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
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
BATCH_SIZE = int(os.getenv('OCR_BATCH_SIZE', 50))
RATE_LIMIT_DELAY = 2  # Delay between API calls (seconds)

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Gemini prompt optimized for job posts
GEMINI_PROMPT = """Extract ALL text from this job posting image. Focus on:
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


def extract_text_gemini(image_path, api_key):
    """Extract text using Google Gemini Vision API"""
    try:
        img_data = encode_image(image_path)
        
        # Gemini API endpoint
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        
        payload = {
            "contents": [{
                "parts": [
                    {"text": GEMINI_PROMPT},
                    {
                        "inline_data": {
                            "mime_type": "image/jpeg",
                            "data": img_data
                        }
                    }
                ]
            }]
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            if 'candidates' in result and len(result['candidates']) > 0:
                extracted_text = result['candidates'][0]['content']['parts'][0]['text']
                return extracted_text, 'gemini'
            else:
                logging.error(f"No candidates in Gemini response for {image_path.name}")
                return None, 'error'
        else:
            logging.error(f"Gemini API error for {image_path.name}: {response.status_code} - {response.text}")
            return None, 'error'
    
    except Exception as e:
        logging.error(f"Gemini API error for {image_path.name}: {e}")
        return None, 'error'


def process_images():
    """Main OCR processing function"""
    logging.info("Starting Gemini OCR processing...")
    
    # Get list of images
    image_files = sorted(INPUT_DIR.glob('*.jpg'))
    total_images = len(image_files)
    
    if total_images == 0:
        logging.error(f"No images found in {INPUT_DIR}")
        return 0
    
    logging.info(f"Found {total_images} images to process")
    
    if not GEMINI_API_KEY:
        logging.error("GEMINI_API_KEY not found in .env file")
        return 0
    
    logging.info("Using Google Gemini Vision API for OCR")
    
    processed = 0
    errors = 0
    
    # Statistics
    stats = {
        'total': total_images,
        'gemini_success': 0,
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
            
            # Extract text using Gemini
            extracted_text, method = extract_text_gemini(image_file, GEMINI_API_KEY)
            
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
                stats['gemini_success'] += 1
                
                logging.debug(f"Processed: {image_file.name} ({method})")
            
            else:
                errors += 1
                stats['errors'] += 1
                logging.error(f"Failed to extract text from {image_file.name}")
            
            pbar.update(1)
            time.sleep(RATE_LIMIT_DELAY)  # Rate limiting
    
    # Summary
    logging.info(f"✅ Gemini OCR Processing Complete")
    logging.info(f"   Total: {total_images}")
    logging.info(f"   Processed: {processed}")
    logging.info(f"   Gemini Success: {stats['gemini_success']}")
    logging.info(f"   Skipped: {stats['skipped']}")
    logging.info(f"   Errors: {errors}")
    
    # Save stats
    stats_file = OUTPUT_DIR / 'processing_stats.json'
    with open(stats_file, 'w') as f:
        json.dump(stats, f, indent=2)
    
    return processed


if __name__ == '__main__':
    print("=" * 60)
    print("🔍 StructCrew Gemini OCR Text Extractor")
    print("=" * 60)
    print(f"Input: {INPUT_DIR}")
    print(f"Output: {OUTPUT_DIR}")
    print(f"Method: Google Gemini 1.5 Flash")
    print("=" * 60)
    print()
    
    result = process_images()
    
    print()
    print("=" * 60)
    print(f"✅ Processing complete! Extracted text from {result} images")
    print("=" * 60)
