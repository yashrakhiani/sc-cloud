# 📤 UPLOAD TO GITHUB - MANUAL METHOD (5 MINUTES)

## Your GitHub repo: https://github.com/yashrakhiani/sc-cloud

The API upload failed. Let's use the web interface - it's actually faster!

---

## 🚀 METHOD 1: Upload All Files at Once (FASTEST)

### Step 1: Create a ZIP of Your Project

1. Open your project folder: `C:\Users\Asus\Desktop\StructCrew_LeadGen`
2. Select ALL files EXCEPT:
   - `.git` folder
   - `data` folder
   - `.env` file
   - `__pycache__` folders
   - `logs` folder
   - `.venv` folder
3. Right-click → **Send to** → **Compressed (zipped) folder**
4. Name it: `leadgen.zip`

### Step 2: Upload to GitHub

1. Go to: https://github.com/yashrakhiani/sc-cloud
2. Click **"uploading an existing file"** link (in the middle of the page)
3. Drag and drop `leadgen.zip`
4. **Commit message**: "Add lead gen pipeline"
5. Click **"Commit changes"**

### Step 3: Extract the ZIP on GitHub

GitHub will show the ZIP file. You need to:
1. Delete the ZIP
2. Upload the actual files

**OR** use Method 2 below (upload files directly)

---

## 🚀 METHOD 2: Upload Files Directly (RECOMMENDED)

### Step 1: Upload Main Files

1. Go to: https://github.com/yashrakhiani/sc-cloud
2. Click **"Add file"** → **"Upload files"**
3. Drag these files from your project folder:
   - `daily_runner.py`
   - `requirements.txt`
   - `Dockerfile`
   - `render.yaml`
   - `.gitignore`
   - `followup_campaign.py`
   - `send_emails_simple.py`
   - `check_results.py`
   - All `.md` files (README, etc.)
4. **Commit message**: "Add main files"
5. Click **"Commit changes"**

### Step 2: Upload Folders

For each folder, repeat:

**Upload `1_scraper` folder:**
1. Click **"Add file"** → **"Upload files"**
2. Drag all files from `1_scraper` folder
3. In the file path box, type: `1_scraper/`
4. Commit

**Upload `2_ocr` folder:**
1. Click **"Add file"** → **"Upload files"**
2. Drag all files from `2_ocr` folder
3. In the file path box, type: `2_ocr/`
4. Commit

**Upload `3_email_extractor` folder:**
1. Click **"Add file"** → **"Upload files"**
2. Drag all files from `3_email_extractor` folder
3. In the file path box, type: `3_email_extractor/`
4. Commit

**Upload `4_email_sender` folder:**
1. Click **"Add file"** → **"Upload files"**
2. Drag all files from `4_email_sender` folder
3. In the file path box, type: `4_email_sender/`
4. Commit

**Upload `templates` folder:**
1. Click **"Add file"** → **"Upload files"**
2. Drag all files from `templates` folder
3. In the file path box, type: `templates/`
4. Commit

---

## 🚀 METHOD 3: Use GitHub Desktop (EASIEST!)

### Step 1: Download GitHub Desktop
https://desktop.github.com

### Step 2: Clone Your Repo
1. Open GitHub Desktop
2. File → Clone repository
3. URL: `https://github.com/yashrakhiani/sc-cloud`
4. Clone

### Step 3: Copy Files
1. Open the cloned folder
2. Copy ALL files from `C:\Users\Asus\Desktop\StructCrew_LeadGen`
3. Paste into the cloned folder
4. **DON'T copy**: `.git`, `data`, `.env`, `logs`, `.venv`

### Step 4: Commit and Push
1. In GitHub Desktop, you'll see all changes
2. Write commit message: "Add lead gen pipeline"
3. Click **"Commit to main"**
4. Click **"Push origin"**

**DONE!** ✅

---

## 🎯 WHICH METHOD?

**Fastest**: Method 3 (GitHub Desktop) - 5 minutes
**No install**: Method 2 (Web upload) - 10 minutes
**Simplest**: Method 1 (ZIP) - but needs extraction

---

## ✅ AFTER UPLOAD

Once files are on GitHub:
1. Go to: https://github.com/yashrakhiani/sc-cloud
2. You should see all your files!
3. **THEN DEPLOY ON RAILWAY!** 🚀

---

## 💡 MY RECOMMENDATION

**Use GitHub Desktop** (Method 3):
- Download: https://desktop.github.com
- Clone repo
- Copy files
- Push
- Done in 5 minutes!

**Which method do you want to use?** Let me know and I'll help! 🎯
