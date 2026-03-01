# Setup Google Drive Model Hosting

## Step 1: Upload Model to Google Drive

1. Go to [Google Drive](https://drive.google.com)
2. Create a new folder (optional, for organization)
3. Upload `model_15.pth` (105MB file)
4. Wait for upload to complete

## Step 2: Get Shareable Link

1. Right-click on `model_15.pth` in Google Drive
2. Click **"Get link"** or **"Share"**
3. Change permission to **"Anyone with the link"** (Viewer)
4. Copy the link

The link will look like:
```
https://drive.google.com/file/d/1ABC123xyz789DEF456ghi012JKL345mno/view?usp=sharing
```

## Step 3: Extract File ID

From the link above, extract the File ID:
- File ID is the part between `/d/` and `/view`
- Example: `1ABC123xyz789DEF456ghi012JKL345mno`

## Step 4: Update app.py

1. Open `app.py` in your editor
2. Find this line (around line 477):
   ```python
   GOOGLE_DRIVE_FILE_ID = "YOUR_GOOGLE_DRIVE_FILE_ID_HERE"
   ```
3. Replace `YOUR_GOOGLE_DRIVE_FILE_ID_HERE` with your actual file ID:
   ```python
   GOOGLE_DRIVE_FILE_ID = "1ABC123xyz789DEF456ghi012JKL345mno"
   ```

## Step 5: Push to GitHub

```bash
cd deepfake-detector
git add app.py
git commit -m "Add Google Drive file ID for model"
git push origin main
```

## Step 6: Redeploy on Streamlit

1. Go to Streamlit Community Cloud
2. Your app should auto-update, or click **"Reboot app"**
3. The app will download the model on first use

## Important Notes

- **File must be publicly accessible** (Anyone with the link)
- **File ID is case-sensitive** - copy it exactly
- **First download takes time** - model is 105MB
- **Model is cached** - subsequent loads are faster

## Troubleshooting

**If download fails:**
- Verify file is set to "Anyone with the link"
- Check file ID is correct
- Make sure `gdown` is in requirements.txt (already added)

**If file ID doesn't work:**
- Try using the full Google Drive URL format:
  ```python
  url = f'https://drive.google.com/uc?export=download&id={GOOGLE_DRIVE_FILE_ID}'
  ```
