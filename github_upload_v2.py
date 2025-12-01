"""
GitHub Upload Script - Fixed Version
Uploads all project files to GitHub using the API with proper error handling
"""

import os
import requests
import base64
from pathlib import Path
import time

# Configuration
GITHUB_TOKEN = "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"
REPO_OWNER = "yashrakhiani"
REPO_NAME = "sc-cloud"
GITHUB_API = "https://api.github.com"
BRANCH = "main"

# Files and folders to skip
SKIP_PATTERNS = [
    '.git', '__pycache__', '.venv', 'data', '.env',
    'logs', '.pyc', 'WEB_UPLOAD.md', 'PUSH_OPTIONS.md',
    'USE_TOKEN.md', 'GITLAB_FIX.md', 'gitlab_upload.py',
    'github_upload.py', 'GITHUB_UPLOAD_HELP.md', 'UPLOAD_TO_GITHUB.md',
    'RAILWAY_FROM_GITLAB.md', 'github_upload_v2.py'
]

def should_skip(path):
    """Check if file/folder should be skipped"""
    path_str = str(path)
    return any(pattern in path_str for pattern in SKIP_PATTERNS)

def get_file_sha(file_path):
    """Get the SHA of an existing file"""
    url = f"{GITHUB_API}/repos/{REPO_OWNER}/{REPO_NAME}/contents/{file_path}"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get('sha')
    return None

def upload_file(file_path, content):
    """Upload or update a single file to GitHub"""
    # Encode content to base64
    encoded_content = base64.b64encode(content).decode('utf-8')
    
    # Check if file exists
    existing_sha = get_file_sha(file_path)
    
    # Prepare API request
    url = f"{GITHUB_API}/repos/{REPO_OWNER}/{REPO_NAME}/contents/{file_path}"
    
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    
    data = {
        "message": f"Update {file_path}" if existing_sha else f"Add {file_path}",
        "content": encoded_content,
        "branch": BRANCH
    }
    
    # Add SHA if file exists (for update)
    if existing_sha:
        data["sha"] = existing_sha
    
    response = requests.put(url, headers=headers, json=data)
    
    if response.status_code in [201, 200]:
        action = "Updated" if existing_sha else "Uploaded"
        print(f"✅ {action}: {file_path}")
        return True
    else:
        print(f"❌ Failed: {file_path}")
        print(f"   Status: {response.status_code}")
        if response.status_code != 404:
            try:
                error_msg = response.json().get('message', 'Unknown error')
                print(f"   Error: {error_msg}")
            except:
                print(f"   Response: {response.text[:200]}")
        return False

def upload_all_files():
    """Upload all project files"""
    print("=" * 60)
    print("📤 Uploading to GitHub: sc-cloud")
    print("=" * 60)
    print()
    
    project_root = Path.cwd()
    uploaded = 0
    failed = 0
    skipped = 0
    
    # Collect all files first
    files_to_upload = []
    for file_path in project_root.rglob('*'):
        if file_path.is_file() and not should_skip(file_path):
            files_to_upload.append(file_path)
    
    print(f"Found {len(files_to_upload)} files to upload")
    print()
    
    # Upload files
    for i, file_path in enumerate(files_to_upload, 1):
        try:
            # Read file content
            with open(file_path, 'rb') as f:
                content = f.read()
            
            # Skip if file is too large (>1MB)
            if len(content) > 1024 * 1024:
                print(f"⚠️  Skipped (too large): {file_path.name}")
                skipped += 1
                continue
            
            # Get relative path
            relative_path = file_path.relative_to(project_root)
            
            # Upload
            print(f"[{i}/{len(files_to_upload)}] ", end="")
            if upload_file(str(relative_path).replace('\\', '/'), content):
                uploaded += 1
            else:
                failed += 1
            
            # Small delay to avoid rate limiting
            time.sleep(0.5)
                
        except Exception as e:
            print(f"❌ Error with {file_path.name}: {e}")
            failed += 1
    
    print()
    print("=" * 60)
    print(f"✅ Upload Complete!")
    print(f"   Uploaded: {uploaded}")
    print(f"   Failed: {failed}")
    print(f"   Skipped: {skipped}")
    print("=" * 60)
    print()
    print("Check your repo: https://github.com/yashrakhiani/sc-cloud")
    print()
    
    if uploaded > 0:
        print("🚀 Ready to deploy on Railway!")
        print("   1. Go to: https://railway.app")
        print("   2. Deploy from GitHub repo: sc-cloud")
        print("   3. Add environment variables")
        print("   4. Done!")

if __name__ == '__main__':
    upload_all_files()
