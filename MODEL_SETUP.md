# Model File Setup Guide

## Issue
The `model_15.pth` file in this directory is currently a Git LFS pointer file (134 bytes), not the actual model file (~110MB). This is why the app cannot load the model.

## Solutions

### Option 1: Download from Git Repository (if available)
If this project is in a Git repository with Git LFS enabled:

```bash
# Navigate to the project root (where .git folder is)
cd /path/to/project/root

# Pull the actual model file using Git LFS
git lfs pull

# Or if you're cloning fresh:
git clone <repository-url>
cd <repository-name>
git lfs pull
```

### Option 2: Download from Original Source
If you have access to the original source (Google Drive, Dropbox, etc.), download the actual `model_15.pth` file (should be ~110MB) and place it in the `deepfake-detector` directory.

### Option 3: Train Your Own Model
Train the model using the provided `Train.ipynb` notebook:

1. Open `Train.ipynb` in Jupyter Notebook or Google Colab
2. Follow the training steps in the notebook
3. The notebook will save the trained model as `model_15.pth`
4. Copy the trained model file to this directory

### Option 4: Use a Pre-trained Model from Another Source
If you have access to another trained VGG16 deepfake detection model with the same architecture, you can use that instead. Just make sure:
- The model architecture matches (VGG16 with the same classifier structure)
- The model file is saved in PyTorch format (.pth)
- Update the path in `app.py` if using a different filename

## Verify Model File
After obtaining the model file, verify it's the correct size:

```bash
ls -lh model_15.pth
```

The file should be approximately **110MB** (not 134 bytes).

## Test the App
Once you have the actual model file:

```bash
cd deepfake-detector
source venv/bin/activate
streamlit run app.py
```

The app should now load the model successfully!
