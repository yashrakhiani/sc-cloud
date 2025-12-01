# 🔑 GitLab Push - Use Personal Access Token

## The authentication in browser didn't work. Let's use a token instead!

---

## STEP 1: Create Personal Access Token (1 minute)

1. **Go to**: https://gitlab.com/-/profile/personal_access_tokens
2. **Token name**: `StructCrew Deploy`
3. **Expiration date**: Select 1 year from now
4. **Select scopes** - Check these boxes:
   - ✅ `api`
   - ✅ `read_repository`
   - ✅ `write_repository`
5. Click **"Create personal access token"**
6. **COPY THE TOKEN** - It looks like: `glpat-xxxxxxxxxxxxxxxxxxxx`
   - ⚠️ You won't see it again, so copy it now!

---

## STEP 2: Push Using Token (30 seconds)

### Option A: Push with Token in URL (Easiest)

Run this command, but **replace YOUR_TOKEN** with the token you just copied:

```bash
git push https://oauth2:YOUR_TOKEN@gitlab.com/yashr.otp-group/structcrew_leadgen.git main
```

**Example**: If your token is `glpat-abc123xyz`, run:
```bash
git push https://oauth2:glpat-abc123xyz@gitlab.com/yashr.otp-group/structcrew_leadgen.git main
```

### Option B: Set Remote with Token

```bash
git remote remove origin
git remote add origin https://oauth2:YOUR_TOKEN@gitlab.com/yashr.otp-group/structcrew_leadgen.git
git push -u origin main
```

---

## ✅ SUCCESS LOOKS LIKE:

```
Enumerating objects: 100, done.
Counting objects: 100% (100/100), done.
Delta compression using up to 8 threads
Compressing objects: 100% (90/90), done.
Writing objects: 100% (100/100), 50.00 KiB | 5.00 MiB/s, done.
Total 100 (delta 5), reused 0 (delta 0), pack-reused 0
To https://gitlab.com/yashr.otp-group/structcrew_leadgen.git
 * [new branch]      main -> main
```

**Then you're done!** ✅

---

## 🎯 QUICK STEPS:

1. Create token: https://gitlab.com/-/profile/personal_access_tokens
2. Copy the token
3. Run: `git push https://oauth2:YOUR_TOKEN@gitlab.com/yashr.otp-group/structcrew_leadgen.git main`

**That's it!** 🚀

---

## 📞 AFTER PUSHING

Once the push succeeds:
1. Go to: https://gitlab.com/yashr.otp-group/structcrew_leadgen
2. You should see all your files there!
3. Then we'll deploy on Render!

---

**Create the token and let me know when you have it!** 🔑
