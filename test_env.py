"""
Test Environment Variables
Quick script to check if Railway can see the environment variables
"""

import os
from dotenv import load_dotenv

load_dotenv()

print("=" * 60)
print("🔍 ENVIRONMENT VARIABLES CHECK")
print("=" * 60)
print()

# Check all important variables
variables = {
    'GMAIL_APP_PASSWORD': os.getenv('GMAIL_APP_PASSWORD', 'NOT SET'),
    'FROM_EMAIL': os.getenv('FROM_EMAIL', 'NOT SET'),
    'DAILY_EMAIL_LIMIT': os.getenv('DAILY_EMAIL_LIMIT', 'NOT SET'),
    'GEMINI_API_KEY': os.getenv('GEMINI_API_KEY', 'NOT SET'),
    'INSTAGRAM_LOGIN_USER': os.getenv('INSTAGRAM_LOGIN_USER', 'NOT SET'),
}

for key, value in variables.items():
    if value == 'NOT SET':
        print(f"❌ {key}: NOT SET")
    else:
        # Mask sensitive values
        if 'PASSWORD' in key or 'KEY' in key:
            masked = value[:4] + '****' + value[-4:] if len(value) > 8 else '****'
            print(f"✅ {key}: {masked}")
        else:
            print(f"✅ {key}: {value}")

print()
print("=" * 60)

# Check if Gmail password is actually set
gmail_pass = os.getenv('GMAIL_APP_PASSWORD', '')
if gmail_pass:
    print(f"✅ Gmail App Password is SET ({len(gmail_pass)} characters)")
    print(f"   First 4 chars: {gmail_pass[:4]}")
    print(f"   Last 4 chars: {gmail_pass[-4:]}")
else:
    print("❌ Gmail App Password is NOT SET!")
    print()
    print("TO FIX:")
    print("1. Go to Railway dashboard")
    print("2. Click on your service")
    print("3. Click 'Variables' tab")
    print("4. Add: GMAIL_APP_PASSWORD = wqdy xnsf zwel kexh")
    print("5. Service will restart automatically")

print("=" * 60)
