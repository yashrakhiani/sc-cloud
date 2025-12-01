# 🚀 DEPLOY TO RENDER WITH GITLAB (5 MINUTES)

## ✅ DONE SO FAR:
- ✅ Render account created
- ✅ GitLab logged in
- ✅ Git repository initialized
- ✅ Code committed

---

## 📋 STEP 1: Create GitLab Repository (1 minute)

### Option A: Via GitLab Website
1. Go to: https://gitlab.com/projects/new
2. Click **"Create blank project"**
3. **Project name**: `StructCrew_LeadGen`
4. **Visibility**: Choose **Private** (recommended)
5. **Uncheck** "Initialize repository with a README"
6. Click **"Create project"**

### Option B: Via Command Line (Faster!)
GitLab will show you the commands after creating the project.

---

## 📋 STEP 2: Push to GitLab (1 minute)

After creating the project, GitLab shows you commands. Use these:

```bash
git remote add origin https://gitlab.com/YOUR_USERNAME/StructCrew_LeadGen.git
git branch -M main
git push -u origin main
```

**⚠️ Replace `YOUR_USERNAME` with your GitLab username!**

### If GitLab asks for credentials:
- **Username**: Your GitLab username
- **Password**: Use a **Personal Access Token** (not your password)

### To create a Personal Access Token:
1. Go to: https://gitlab.com/-/profile/personal_access_tokens
2. **Token name**: `Render Deploy`
3. **Scopes**: Check `read_repository` and `write_repository`
4. Click **"Create personal access token"**
5. **Copy the token** (you won't see it again!)
6. Use this token as your password when pushing

---

## 📋 STEP 3: Deploy on Render (3 minutes)

### 3.1 Connect GitLab to Render

1. Go to: https://dashboard.render.com
2. Click **"New +"** → **"Background Worker"**
3. Click **"Connect GitLab"** (instead of GitHub)
4. Authorize Render to access your GitLab
5. Select your repository: `StructCrew_LeadGen`
6. Click **"Connect"**

### 3.2 Configure Service

**Name**: `structcrew-leadgen`

**Environment**: `Python 3`

**Build Command**:
```
pip install -r requirements.txt
```

**Start Command**:
```
python daily_runner.py
```

**Instance Type**: `Free`

### 3.3 Add Environment Variables

Click **"Advanced"** → **"Add Environment Variable"**

Add these **one by one** (no quotes!):

```
INSTAGRAM_USERNAME = archijobs
INSTAGRAM_LOGIN_USER = brijeshrajan213
INSTAGRAM_LOGIN_PASS = Yashhk
GEMINI_API_KEY = AIzaSyACWNeMcb4xMCxm8BnSXFS9-S8loUAvEhY
FROM_EMAIL = structcrew@gmail.com
GMAIL_APP_PASSWORD = syjg ogsv wrab uoei
MAX_POSTS = 500
DAILY_EMAIL_LIMIT = 500
HEADLESS = true
USE_CLAUDE = false
VALIDATE_EMAILS = true
```

### 3.4 Deploy!

1. Click **"Create Background Worker"**
2. Wait 2-3 minutes for build
3. Check **"Logs"** tab

---

## 🎯 QUICK COMMANDS FOR YOU

Since you're already logged into GitLab, here's what to run:

### 1. Create the repo on GitLab website first
Go to: https://gitlab.com/projects/new

### 2. Then run these commands:

```bash
# Add GitLab remote (replace YOUR_USERNAME!)
git remote add origin https://gitlab.com/YOUR_USERNAME/StructCrew_LeadGen.git

# Push to GitLab
git branch -M main
git push -u origin main
```

### 3. If it asks for credentials:
- Username: Your GitLab username
- Password: Your Personal Access Token (create at https://gitlab.com/-/profile/personal_access_tokens)

---

## ✅ AFTER PUSHING

You should see:
```
Enumerating objects: 100, done.
Counting objects: 100% (100/100), done.
Writing objects: 100% (100/100), done.
Total 100 (delta 0), reused 0 (delta 0)
To https://gitlab.com/YOUR_USERNAME/StructCrew_LeadGen.git
 * [new branch]      main -> main
```

**Success!** ✅

---

## 📊 THEN: Deploy on Render

1. Go to: https://dashboard.render.com
2. New + → Background Worker
3. Connect GitLab
4. Select your repo
5. Add environment variables
6. Deploy!

---

## 🔧 TROUBLESHOOTING

### "Authentication failed"
- Use Personal Access Token, not password
- Create token at: https://gitlab.com/-/profile/personal_access_tokens
- Scopes needed: `read_repository`, `write_repository`

### "Repository not found"
- Make sure repo is created on GitLab first
- Check the URL is correct
- Verify you're logged into correct GitLab account

### "Render can't find my repo"
- Make sure repo is not empty (we already committed code ✅)
- Refresh Render page
- Try disconnecting and reconnecting GitLab

---

## 🎯 SUMMARY

**What you need to do:**

1. **Create GitLab repo**: https://gitlab.com/projects/new (1 min)
2. **Push code**: Run the git commands above (1 min)
3. **Deploy on Render**: Connect GitLab → Deploy (3 min)

**Total**: 5 minutes! 🚀

---

## 💡 PRO TIP

Save your Personal Access Token somewhere safe! You'll need it for:
- Pushing code
- Updating your pipeline
- Future deployments

---

**Ready? Create the GitLab repo and let's push!** 🎯
