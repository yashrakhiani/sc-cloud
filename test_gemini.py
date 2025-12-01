import requests
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')

print(f"Testing Gemini API...")
print(f"API Key: {api_key[:20]}...")

# Test with a simple text prompt first
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"

payload = {
    "contents": [{
        "parts": [{
            "text": "Say hello!"
        }]
    }]
}

response = requests.post(url, json=payload)

print(f"\nStatus Code: {response.status_code}")
print(f"Response: {response.text[:500]}")

if response.status_code == 200:
    print("\n✅ Gemini API is working!")
else:
    print("\n❌ Gemini API error - checking alternative models...")
    
    # Try gemini-pro model
    url2 = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
    response2 = requests.post(url2, json=payload)
    print(f"\nGemini Pro Status: {response2.status_code}")
    print(f"Response: {response2.text[:300]}")
