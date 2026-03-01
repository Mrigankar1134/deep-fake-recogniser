# Troubleshooting Streamlit Deployment

## Issue: Failed to Clone Repository

If you're seeing "Failed to download the sources" error, try these solutions:

### Solution 1: Verify Repository is Public

1. Go to your repository: https://github.com/Mrigankar1134/deep-fake-recogiser
2. Click **Settings** (top right)
3. Scroll down to **Danger Zone**
4. Make sure the repository is set to **Public** (not Private)
5. If it's private, change it to public (required for free Streamlit hosting)

### Solution 2: Check Repository Name in Streamlit

When deploying on Streamlit Community Cloud:
- Make sure you select the exact repository: `Mrigankar1134/deep-fake-recogiser`
- Check for any typos
- The repository name is case-sensitive

### Solution 3: Git LFS Issue

If Git LFS is causing issues, you can temporarily remove it:

```bash
# Option A: Remove Git LFS tracking (if model file causes issues)
git lfs untrack "*.pth"
git rm --cached model_15.pth
git add model_15.pth
git commit -m "Remove Git LFS, use regular file"
git push
```

**OR** host the model separately and download it in the app.

### Solution 4: Reboot the App

1. Go to Streamlit Community Cloud dashboard
2. Find your app
3. Click the **⋮** (three dots) menu
4. Select **Reboot app**

### Solution 5: Check Repository Access

Make sure:
- You're signed into Streamlit with the same GitHub account
- The GitHub account has access to the repository
- The repository exists and has content

### Solution 6: Verify Files Are Pushed

Check that all files are in the repository:
- Visit: https://github.com/Mrigankar1134/deep-fake-recogiser
- Verify you see: `app.py`, `requirements.txt`, etc.
- Make sure the `main` branch has content

### Solution 7: Try Manual Repository Selection

In Streamlit Community Cloud:
1. Delete the failed app
2. Create a new app
3. Manually type or select: `Mrigankar1134/deep-fake-recogiser`
4. Branch: `main`
5. Main file: `app.py`

### Solution 8: Check Git LFS on Streamlit

If Git LFS is the issue, Streamlit Cloud might not support it well. Consider:

**Alternative: Host Model on Cloud Storage**

1. Upload `model_15.pth` to Google Drive
2. Get a shareable link
3. Modify `app.py` to download it on first run
4. Add `gdown` to requirements.txt

Example code to add to `load_model()`:
```python
import gdown

if not os.path.exists('model_15.pth'):
    url = "YOUR_GOOGLE_DRIVE_LINK"
    gdown.download(url, 'model_15.pth', quiet=False)
```

### Quick Fix Checklist

- [ ] Repository is **Public**
- [ ] Repository name is correct: `Mrigankar1134/deep-fake-recogiser`
- [ ] Branch is `main`
- [ ] Main file is `app.py`
- [ ] All files are pushed to GitHub
- [ ] Tried rebooting the app
- [ ] Signed in with correct GitHub account

If none of these work, check the Streamlit Community Cloud logs for more specific error messages.
