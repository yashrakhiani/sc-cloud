# Use official Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
# - tesseract-ocr: For text extraction
# - chromium: For Playwright scraping
# - cron: For scheduling (optional)
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    chromium \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers
RUN playwright install --with-deps chromium

# Install spaCy model
RUN python -m spacy download en_core_web_sm

# Copy application code
COPY . .

# Create directories for data persistence
RUN mkdir -p data/raw_images data/extracted_text logs

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV HEADLESS=true

# Run the daily automation script
CMD ["python", "daily_runner.py"]
