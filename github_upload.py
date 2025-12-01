"""
GitHub Auto-Upload Script
Uploads all project files to GitHub using the API
"""

import os
import requests
import base64
from pathlib import Path

# Configuration
GITHUB_TOKEN = "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"
REPO_OWNER = "yashrakhiani"
REPO_NAME = "sc-cloud"
GITHUB_API = "https://api.github.com"

# Files and folders to skip
SKIP_PATTERNS = [
    '.git', '__pycache__', '.venv', 'data', '.env',
    'logs', '.pyc', 'WEB_UPLOAD.md', 'PUSH_OPTIONS.md',
    'USE_TOKEN.md', 'GITLAB_FIX.md', 'gitlab_upload.py',
    'github_upload.py', 'GITHUB_UPLOAD_HELP.md'
]

def should_skip(path):
    """Check if file/folder should be skipped"""
    path_str = str(path)
    return any(pattern in path_str for pattern in SKIP_PATTERNS)

def upload_file(file_path, content):
    """Upload a single file to GitHub"""
    # Encode content to base64
    encoded_content = base64.b64encode(content).decode('utf-8')
    
    # Prepare API request
    url = f"{GITHUB_API}/repos/{REPO_OWNER}/{REPO_NAME}/contents/{file_path}"
    
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    data = {
        "message": f"Add {file_path}",
        "content": encoded_content,
        "branch": "main"
    }
    
    response = requests.put(url, headers=headers, json=data)
    
    if response.status_code in [201, 200]:
        print(f"✅ Uploaded: {file_path}")
        return True
    elif response.status_code == 422:
        # File already exists, try to update
        sha = response.json().get('message', '')
        if 'sha' in sha:
            return True
        print(f"⚠️  Skipped (exists): {file_path}")
        return True
    else:
        print(f"❌ Failed: {file_path} - {response.status_code}")
        print(f"   Error: {response.text[:200]}")
        return False

def upload_all_files():
    """Upload all project files"""
    print("=" * 60)
    print("📤 Uploading to GitHub...")
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
    print("Check your repo: https://github.com/yashrakhiani/sc-cloud")

if __name__ == '__main__':
    upload_all_files()
