"""
GitLab Auto-Upload Script
Uploads all project files to GitLab using the API
"""

import os
import requests
import base64
from pathlib import Path

# Configuration
GITLAB_TOKEN = "glpat-zi0BdSMe0QI7zKBdSc2--G86MQp1OmoxYzE1Cw.01.120zzcg7s"
PROJECT_ID = "yashr.otp-group/structcrew_leadgen"
GITLAB_API = "https://gitlab.com/api/v4"

# Files and folders to skip
SKIP_PATTERNS = [
    '.git', '__pycache__', '.venv', 'data', '.env',
    'logs', '.pyc', 'WEB_UPLOAD.md', 'PUSH_OPTIONS.md',
    'USE_TOKEN.md', 'GITLAB_FIX.md', 'gitlab_upload.py'
]

def should_skip(path):
    """Check if file/folder should be skipped"""
    path_str = str(path)
    return any(pattern in path_str for pattern in SKIP_PATTERNS)

def upload_file(file_path, content):
    """Upload a single file to GitLab"""
    # Encode content to base64
    encoded_content = base64.b64encode(content).decode('utf-8')
    
    # Prepare API request
    url = f"{GITLAB_API}/projects/{PROJECT_ID.replace('/', '%2F')}/repository/files/{file_path.replace('/', '%2F')}"
    
    headers = {
        "PRIVATE-TOKEN": GITLAB_TOKEN,
        "Content-Type": "application/json"
    }
    
    data = {
        "branch": "main",
        "content": encoded_content,
        "commit_message": f"Add {file_path}",
        "encoding": "base64"
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code in [201, 200]:
        print(f"✅ Uploaded: {file_path}")
        return True
    else:
        print(f"❌ Failed: {file_path} - {response.status_code}")
        print(f"   Error: {response.text}")
        return False

def upload_all_files():
    """Upload all project files"""
    print("=" * 60)
    print("📤 Uploading to GitLab...")
    print("=" * 60)
    print()
    
    project_root = Path.cwd()
    uploaded = 0
    failed = 0
    
    # Get all files
    for file_path in project_root.rglob('*'):
        if file_path.is_file() and not should_skip(file_path):
            try:
                # Read file content
                with open(file_path, 'rb') as f:
                    content = f.read()
                
                # Get relative path
                relative_path = file_path.relative_to(project_root)
                
                # Upload
                if upload_file(str(relative_path).replace('\\', '/'), content):
                    uploaded += 1
                else:
                    failed += 1
                    
            except Exception as e:
                print(f"❌ Error with {file_path}: {e}")
                failed += 1
    
    print()
    print("=" * 60)
    print(f"✅ Upload Complete!")
    print(f"   Uploaded: {uploaded}")
    print(f"   Failed: {failed}")
    print("=" * 60)
    print()
    print("Check your repo: https://gitlab.com/yashr.otp-group/structcrew_leadgen")

if __name__ == '__main__':
    upload_all_files()
