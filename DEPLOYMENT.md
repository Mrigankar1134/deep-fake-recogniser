# How to Deploy Your DeepFake Detector App for Free

## Using Streamlit Community Cloud (Free)

Streamlit Community Cloud offers free hosting for public Streamlit apps. Follow these steps:

### Prerequisites

1. **GitHub Account** - You need a GitHub account (free)
2. **Git Repository** - Your code should be in a GitHub repository

### Step 1: Prepare Your Repository

1. **Create a GitHub repository** (if you haven't already):
   - Go to [GitHub](https://github.com)
   - Click "New repository"
   - Name it (e.g., `deepfake-detector`)
   - Make it **Public** (required for free hosting)
   - Don't initialize with README (if you already have files)

2. **Add your files to GitHub**:
   ```bash
   cd /Users/mrigankarsonowal/Documents/deepfake-detector-model/deepfake-detector
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/deepfake-detector.git
   git push -u origin main
   ```

### Step 2: Create requirements.txt

Make sure your `requirements.txt` file is in the root directory and includes all dependencies:

```
torch
torchvision
numpy
pandas
scikit-learn
Pillow
matplotlib
streamlit
```

### Step 3: Important - Handle the Model File

**The model file (`model_15.pth`) is ~110MB, which is too large for GitHub.**

You have a few options:

#### Option A: Use Git LFS (Recommended)
```bash
# Install Git LFS if not already installed
brew install git-lfs  # On Mac
# or download from https://git-lfs.github.com

# Initialize Git LFS
git lfs install

# Track the model file
git lfs track "*.pth"

# Add the .gitattributes file
git add .gitattributes

# Add and commit the model file
git add model_15.pth
git commit -m "Add model file via Git LFS"
git push
```

#### Option B: Host Model on Cloud Storage
- Upload `model_15.pth` to Google Drive, Dropbox, or AWS S3
- Modify `app.py` to download the model on first run
- Add download code in the `load_model()` function

#### Option C: Use a Smaller Model
- Train a smaller model or use model compression

### Step 4: Deploy to Streamlit Community Cloud

1. **Go to Streamlit Community Cloud**:
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account

2. **Deploy Your App**:
   - Click "New app"
   - Select your GitHub repository
   - Choose the branch (usually `main`)
   - Set the main file path: `app.py`
   - Click "Deploy"

3. **Wait for Deployment**:
   - Streamlit will install dependencies and deploy your app
   - This usually takes 2-5 minutes
   - You'll get a URL like: `https://your-app-name.streamlit.app`

### Step 5: Configure App Settings (if needed)

If your app needs environment variables or special settings:
- Go to your app's settings in Streamlit Community Cloud
- Add any required environment variables
- Adjust resource limits if needed

### Important Notes

1. **Model File Size**: 
   - Free tier has limits on file sizes
   - Git LFS helps but may have bandwidth limits
   - Consider hosting the model separately if issues occur

2. **Public Repository Required**:
   - Free hosting requires a public GitHub repository
   - Your code will be visible to everyone

3. **Resource Limits**:
   - Free tier has CPU/memory limits
   - Apps may be slower during peak times

4. **Custom Domain**:
   - Free tier doesn't support custom domains
   - You'll get a `*.streamlit.app` URL

### Troubleshooting

**If deployment fails:**
- Check that `requirements.txt` is correct
- Ensure `app.py` is in the root directory
- Verify all imports are in requirements.txt
- Check the deployment logs in Streamlit Community Cloud

**If model loading fails:**
- Verify the model file is accessible
- Check file paths in your code
- Consider using absolute paths or environment variables

### Alternative: Deploy Model Separately

If the model file causes issues, you can:

1. Upload model to Google Drive
2. Get a shareable link
3. Modify `load_model()` to download it:

```python
import gdown

@st.cache_resource
def load_model(path='model_15.pth'):
    # Download from Google Drive if not exists
    if not os.path.exists(path):
        url = "YOUR_GOOGLE_DRIVE_LINK"
        gdown.download(url, path, quiet=False)
    # ... rest of your code
```

Add `gdown` to requirements.txt if using this approach.

### Your App URL

Once deployed, you'll get a URL like:
```
https://deepfake-detector.streamlit.app
```

Share this URL with others to use your app!
