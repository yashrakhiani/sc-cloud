"""
OCR Processor using Claude Vision API
Extracts text from job posting images
"""

import os
import base64
from pathlib import Path
from anthropic import Anthropic
from dotenv import load_dotenv
import json
import logging
from tqdm import tqdm

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('../logs/ocr.log'),
        logging.StreamHandler()
    ]
)

class OCRProcessor:
    def __init__(self):
        self.api_key = os.getenv('ANTHROPIC_API_KEY')
        self.client = Anthropic(api_key=self.api_key)
        self.images_dir = Path('../data/raw_images')
        self.output_dir = Path('../data/extracted_text')
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def encode_image(self, image_path):
        """Encode image to base64"""
        with open(image_path, 'rb') as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    def extract_text_from_image(self, image_path):
        """Use Claude Vision API to extract text from image"""
        logging.info(f"Processing {image_path.name}")
        
        try:
            image_data = self.encode_image(image_path)
            
            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/jpeg",
                                    "data": image_data,
                                },
                            },
                            {
                                "type": "text",
                                "text": "Extract all text from this job posting image. Pay special attention to company names, email addresses, phone numbers, and website URLs. Return the extracted information in a structured format."
                            }
                        ],
                    }
                ],
            )
            
            return message.content[0].text
            
        except Exception as e:
            logging.error(f"Error processing {image_path.name}: {e}")
            return None
    
    def process_all_images(self):
        """Process all images in the raw_images directory"""
        image_files = list(self.images_dir.glob('*.jpg')) + list(self.images_dir.glob('*.png'))
        logging.info(f"Found {len(image_files)} images to process")
        
        for image_path in tqdm(image_files, desc="Processing images"):
            extracted_text = self.extract_text_from_image(image_path)
            
            if extracted_text:
                # Save extracted text
                output_file = self.output_dir / f"{image_path.stem}.txt"
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(extracted_text)
                    
        logging.info("OCR processing complete")

if __name__ == "__main__":
    processor = OCRProcessor()
    processor.process_all_images()
