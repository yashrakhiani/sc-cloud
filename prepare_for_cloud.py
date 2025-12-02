import zipfile
import os
from pathlib import Path

def zip_project():
    output_filename = "structcrew_leadgen_deploy.zip"
    source_dir = Path(".")
    
    # Files/Dirs to exclude
    exclude_dirs = {'.git', '.venv', 'venv', '__pycache__', 'logs', 'data', '.idea', '.vscode'}
    exclude_files = {output_filename, '.env', '.DS_Store'} # Exclude .env for security, user should create it on server
    
    print(f"📦 Zipping project to {output_filename}...")
    
    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            # Modify dirs in-place to skip excluded directories
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            for file in files:
                if file in exclude_files:
                    continue
                if file.endswith('.pyc'):
                    continue
                    
                file_path = Path(root) / file
                archive_name = file_path.relative_to(source_dir)
                
                print(f"  Adding: {archive_name}")
                zipf.write(file_path, archive_name)
                
    print(f"\n✅ Successfully created {output_filename}")
    print(f"👉 Upload this file to your Google Cloud VM.")

if __name__ == "__main__":
    zip_project()
