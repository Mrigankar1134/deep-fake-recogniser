# Quick Deployment Guide

## 🚀 Deploy in 5 Steps

### 1. Push to GitHub
```bash
cd deepfake-detector
git init
git add .
git commit -m "Ready to deploy"
git remote add origin https://github.com/YOUR_USERNAME/deepfake-detector.git
git push -u origin main
```

**Important:** Repository must be **PUBLIC** for free hosting.

### 2. Handle Model File (110MB)

**Option A - Git LFS (Recommended):**
```bash
git lfs install
git lfs track "*.pth"
git add .gitattributes model_15.pth
git commit -m "Add model via Git LFS"
git push
```

**Option B - Skip for now:**
- Comment out model loading temporarily
- Deploy app first to test
- Add model later via cloud storage

### 3. Deploy on Streamlit Cloud

1. Go to: https://share.streamlit.io
2. Sign in with GitHub
3. Click "New app"
4. Select your repository
5. Main file: `app.py`
6. Click "Deploy"

### 4. Wait & Test

- Deployment takes 2-5 minutes
- Check logs if errors occur
- Test your app URL

### 5. Share Your App

Your app will be live at:
```
https://YOUR-APP-NAME.streamlit.app
```

## ⚠️ Common Issues

**Model file too large?**
- Use Git LFS (see Option A above)
- Or host model on Google Drive and download on first run

**Deployment fails?**
- Check `requirements.txt` has all packages
- Verify `app.py` is in root directory
- Check deployment logs for errors

**App runs but model doesn't load?**
- Verify model file path is correct
- Check file permissions
- Consider downloading from cloud storage

## 📝 Files Needed

Make sure these files are in your repo:
- ✅ `app.py` (main app file)
- ✅ `requirements.txt` (dependencies)
- ✅ `model_15.pth` (via Git LFS or cloud)
- ✅ `.gitignore` (optional but recommended)

That's it! Your app should be live in minutes! 🎉
