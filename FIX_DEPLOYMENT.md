# Fix Deployment Issue

## Problem: Streamlit Cloud can't clone repository

Since your repository is already public, the issue is likely one of these:

### Solution 1: Verify Repository Name in Streamlit (Most Common)

When creating the app in Streamlit Community Cloud, make sure you:

1. **Type the repository name exactly**: `Mrigankar1134/deep-fake-recogiser`
   - Check for typos
   - Make sure there's a hyphen (not underscore) in "deep-fake-recogiser"
   - Case-sensitive: `Mrigankar1134` (capital M)

2. **Or use the dropdown** to select from your repositories instead of typing

3. **Branch**: Make sure it's `main` (not `master`)

### Solution 2: Remove Git LFS (If Model File Causes Issues)

Streamlit Cloud sometimes has issues with Git LFS. Try this:

```bash
cd deepfake-detector
git lfs untrack "*.pth"
git rm --cached model_15.pth
git add model_15.pth
git commit -m "Remove Git LFS for model file"
git push
```

**Note**: This will make the model file part of regular git, which might be slow but should work.

### Solution 3: Host Model Separately (Recommended for Large Files)

Instead of using Git LFS, host the model on cloud storage:

1. **Upload model to Google Drive**:
   - Upload `model_15.pth` to Google Drive
   - Right-click → Get link → Make it shareable
   - Copy the file ID from the link

2. **Update app.py** to download model:

Add this at the top of your `load_model()` function:

```python
import gdown

@st.cache_resource
def load_model(path='model_15.pth'):
    # Download model if not exists
    if not os.path.exists(path):
        with st.spinner("Downloading model file..."):
            # Replace YOUR_FILE_ID with the Google Drive file ID
            url = 'https://drive.google.com/uc?id=YOUR_FILE_ID'
            gdown.download(url, path, quiet=False)
    
    # Rest of your existing code...
```

3. **Add gdown to requirements.txt**:
```
gdown
```

4. **Remove model from git**:
```bash
git rm --cached model_15.pth
echo "model_15.pth" >> .gitignore
git add .gitignore
git commit -m "Remove model file, host on Google Drive"
git push
```

### Solution 4: Check Streamlit App Settings

1. Go to your Streamlit Community Cloud dashboard
2. Click on your app
3. Go to **Settings**
4. Verify:
   - Repository: `Mrigankar1134/deep-fake-recogiser`
   - Branch: `main`
   - Main file: `app.py`

### Solution 5: Delete and Recreate App

1. Delete the failed app in Streamlit
2. Create a new app
3. Select repository from dropdown (don't type)
4. Choose `main` branch
5. Main file: `app.py`

### Quick Test

To verify your repository is accessible, try cloning it yourself:

```bash
git clone https://github.com/Mrigankar1134/deep-fake-recogiser.git test-clone
cd test-clone
ls -la
```

If this works, the repository is fine and the issue is with Streamlit's access.

## Recommended Approach

**Best solution**: Use Solution 3 (host model separately) because:
- Avoids Git LFS issues
- Faster deployments
- Model file doesn't count against repository size
- More reliable on Streamlit Cloud

Would you like me to help you set up the Google Drive hosting for the model file?
