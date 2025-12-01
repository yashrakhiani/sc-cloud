import sqlite3
import json
from pathlib import Path

# Check OCR stats
stats_file = Path('data/extracted_text/processing_stats.json')
if stats_file.exists():
    with open(stats_file) as f:
        stats = json.load(f)
    print("\n📊 OCR PROCESSING STATS:")
    print("="*60)
    for key, value in stats.items():
        print(f"  {key}: {value}")
    print("="*60)

# Check database
db_file = Path('data/leads.db')
if db_file.exists():
    conn = sqlite3.connect('data/leads.db')
    cursor = conn.cursor()
    
    # Total leads
    cursor.execute('SELECT COUNT(*) FROM leads')
    total = cursor.fetchone()[0]
    
    print(f"\n🎯 LEADS DATABASE:")
    print("="*60)
    print(f"Total Leads Found: {total}")
    
    if total > 0:
        # By status
        cursor.execute('SELECT status, COUNT(*) FROM leads GROUP BY status')
        print("\nBy Status:")
        for row in cursor.fetchall():
            print(f"  {row[0]}: {row[1]}")
        
        # Sample leads
        cursor.execute('SELECT company, email, phone, website FROM leads LIMIT 5')
        print("\n📧 Sample Leads:")
        print("="*60)
        for i, row in enumerate(cursor.fetchall(), 1):
            print(f"\nLead #{i}:")
            print(f"  Company: {row[0]}")
            print(f"  Email: {row[1]}")
            print(f"  Phone: {row[2]}")
            print(f"  Website: {row[3]}")
    
    conn.close()
    print("="*60)

# Check extracted text files
text_dir = Path('data/extracted_text')
text_files = list(text_dir.glob('*.txt'))
print(f"\n📄 Extracted Text Files: {len(text_files)}")

# Check logs
log_file = Path('logs/ocr.log')
if log_file.exists():
    with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
        print(f"\n📋 Last OCR Log Entries:")
        print("="*60)
        for line in lines[-10:]:
            print(line.strip())
        print("="*60)
