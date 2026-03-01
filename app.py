import streamlit as st
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import io
import os
try:
    import gdown
except ImportError:
    gdown = None

# Page configuration
st.set_page_config(
    page_title="DeepFake Detector",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items=None
)

# Custom CSS - Clean 2-color design
st.markdown("""
    <style>
    /* Hide Streamlit menu but keep sidebar toggle */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    /* Keep header visible for sidebar toggle - don't hide it */
    /* The sidebar toggle button is in the header */
    
    /* ============================================
       ALL WHITE BACKGROUNDS, ALL BLACK TEXT
       ============================================ */
    
    /* Global - ALL backgrounds white */
    .stApp, body, html, [data-testid="stAppViewContainer"],
    [data-testid="stSidebar"], [data-testid="stSidebar"] > div,
    .main-container, .sidebar-content, .confidence-section,
    .image-container, .prediction-card, .modal-content,
    [data-baseweb="base-input"], [data-baseweb="select"],
    .stSelectbox, .stTextInput, .stCheckbox,
    [class*="st"], [class*="element-container"] {
        background: #ffffff !important;
        background-color: #ffffff !important;
    }
    
    /* Sidebar background white - comprehensive */
    section[data-testid="stSidebar"],
    section[data-testid="stSidebar"] > div,
    [data-testid="stSidebar"] .css-1d391kg,
    [data-testid="stSidebar"] .css-1lcbmhc,
    [data-testid="stSidebar"] [class*="css"] {
        background-color: #ffffff !important;
        background: #ffffff !important;
    }
    
    /* Main app container white */
    [data-testid="stAppViewContainer"],
    [data-testid="stAppViewContainer"] > div {
        background-color: #ffffff !important;
        background: #ffffff !important;
    }
    
    /* ALL text BLACK */
    *, *::before, *::after,
    body, .stApp, .main-container, .sidebar-content,
    p, div, span, label, h1, h2, h3, h4, h5, h6,
    .stMarkdown, .brand-title, .brand-subtitle, .section-title,
    .prediction-label, .prediction-desc, .confidence-label, .confidence-value,
    [data-testid="stSidebar"] *, [data-testid="stSidebar"] p, [data-testid="stSidebar"] div,
    [data-testid="stSidebar"] h3, [data-testid="stSidebar"] label,
    [data-baseweb="file-uploader"] *,
    [data-baseweb="file-uploader"] p,
    [data-baseweb="file-uploader"] span,
    [data-baseweb="file-uploader"] div,
    [data-baseweb="file-uploader"] label {
        color: #000000 !important;
    }
    
    /* ALL icons BLACK */
    svg, [class*="icon"], [data-icon], path {
        fill: #000000 !important;
        stroke: #000000 !important;
        color: #000000 !important;
    }
    
    /* File uploader background white */
    [data-baseweb="file-uploader"],
    [data-baseweb="file-uploader"] > div {
        background-color: #ffffff !important;
        background: #ffffff !important;
        border: 1px solid #e5e5e5 !important;
    }
    
    /* Main container - compact */
    .main-container {
        background: white;
        border-radius: 8px;
        padding: 2rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        margin: 1rem auto;
        max-width: 1200px;
    }
    
    /* Header - minimal */
    .brand-header {
        text-align: center;
        margin-bottom: 2rem;
        padding-bottom: 1.5rem;
        border-bottom: 1px solid #e5e5e5;
    }
    
    .brand-title {
        font-size: 2rem;
        font-weight: 600;
        color: #000000 !important;
        margin-bottom: 0.5rem;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    
    .brand-subtitle {
        font-size: 0.95rem;
        color: #000000 !important;
        font-weight: 400;
    }
    
    /* Prediction cards - clean */
    .prediction-card {
        background: white;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid;
    }
    
    .prediction-real {
        border-left-color: #6b7280;
    }
    
    .prediction-fake {
        border-left-color: #6b7280;
    }
    
    .prediction-label {
        font-size: 1.25rem;
        font-weight: 600;
        margin: 0;
        color: #000000 !important;
    }
    
    .prediction-label-real {
        color: #000000 !important;
    }
    
    .prediction-label-fake {
        color: #000000 !important;
    }
    
    .prediction-desc {
        color: #000000 !important;
        margin: 0.5rem 0 0 0;
        font-size: 0.9rem;
    }
    
    /* Confidence - minimal */
    .confidence-section {
        background: #ffffff !important;
        border: 1px solid #e5e5e5;
        border-radius: 6px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .confidence-label {
        font-size: 0.8rem;
        font-weight: 600;
        color: #000000 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
    }
    
    .confidence-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #000000 !important;
        margin-top: 0.5rem;
    }
    
    /* Progress bar - gray */
    .stProgress > div > div > div {
        background: #6b7280;
    }
    
    /* Image container */
    .image-container {
        background: white;
        border-radius: 8px;
        padding: 1rem;
        border: 1px solid #e5e5e5;
    }
    
    .section-title {
        font-size: 1rem;
        font-weight: 600;
        color: #000000 !important;
        margin-bottom: 1rem;
    }
    
    /* Sidebar - clean */
    .sidebar-content {
        background: white;
        padding: 1rem;
        border-radius: 6px;
        margin-bottom: 1rem;
        border: 1px solid #e5e5e5;
    }
    
    /* Sidebar text - all black */
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] div, 
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] span {
        color: #000000 !important;
    }
    
    /* Sidebar headers */
    [data-testid="stSidebar"] h3 {
        color: #000000 !important;
        font-weight: 600 !important;
    }
    
    /* Compact spacing */
    .element-container {
        margin-bottom: 1rem;
    }
    
    /* File uploader styling */
    .uploadedFile {
        border-radius: 6px;
    }
    
    /* File uploader button - gray with black text */
    .stFileUploader button,
    .stFileUploader button span,
    [data-testid="stFileUploader"] button,
    [data-testid="stFileUploader"] button span {
        color: #000000 !important;
        background-color: #e5e7eb !important;
        border: 1px solid #9ca3af !important;
        font-weight: 600 !important;
    }
    
    .stFileUploader button:hover,
    [data-testid="stFileUploader"] button:hover {
        background-color: #d1d5db !important;
    }
    
    /* File uploader label - black */
    .stFileUploader > label,
    [data-testid="stFileUploader"] > label {
        color: #000000 !important;
        font-weight: 600 !important;
    }
    
    /* File uploader drop zone text - black */
    [data-baseweb="file-uploader"],
    [data-baseweb="file-uploader"] *,
    [data-baseweb="file-uploader"] p,
    [data-baseweb="file-uploader"] span,
    [data-baseweb="file-uploader"] div,
    [data-baseweb="file-uploader"] label {
        color: #000000 !important;
    }
    
    /* Alternative selectors for upload area */
    .stFileUploader [style*="background"],
    .stFileUploader [style*="background"] *,
    .stFileUploader [style*="background"] p,
    .stFileUploader [style*="background"] span {
        color: #ffffff !important;
    }
    
    /* Target any div with dark background in file uploader */
    [data-testid="stFileUploader"] > div > div[style*="background"] *,
    [data-testid="stFileUploader"] > div > div[style*="background"] p,
    [data-testid="stFileUploader"] > div > div[style*="background"] span {
        color: #ffffff !important;
    }
    
    /* Remove extra padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Ensure all Streamlit text elements are visible */
    .stTextInput label, .stSelectbox label, .stCheckbox label {
        color: #000000 !important;
    }
    
    /* Status text visibility */
    .stStatusWidget {
        color: #000000 !important;
    }
    
    /* Caption text */
    .stCaption {
        color: #000000 !important;
    }
    
    /* Expander text */
    .streamlit-expanderHeader {
        color: #000000 !important;
    }
    
    /* Sidebar toggle button - ensure it's visible */
    [data-testid="stSidebar"] [data-testid="baseButton-header"],
    button[data-testid="baseButton-header"],
    [data-testid="collapsedControl"] {
        visibility: visible !important;
        display: block !important;
    }
    
    /* Sidebar toggle button styling - gray */
    [data-testid="collapsedControl"] button {
        background-color: #e5e7eb !important;
        color: #000000 !important;
        border: 1px solid #9ca3af !important;
    }
    
    /* About Creators Button Container */
    .creators-btn-container {
        position: fixed;
        top: 1rem;
        right: 1rem;
        z-index: 1000;
    }
    
    /* Style Streamlit button */
    .creators-btn-container button {
        background-color: #e5e7eb !important;
        color: #000000 !important;
        border: 1px solid #9ca3af !important;
        border-radius: 6px;
        font-weight: 600;
        padding: 0.5rem 1rem;
    }
    
    .creators-btn-container button:hover {
        background-color: #d1d5db !important;
    }
    
    /* Modal/Popup Styles */
    .modal {
        display: none;
        position: fixed;
        z-index: 2000;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.5);
        overflow: auto;
    }
    
    .modal-content {
        background-color: white;
        margin: 5% auto;
        padding: 2rem;
        border-radius: 8px;
        width: 90%;
        max-width: 500px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        position: relative;
    }
    
    .close {
        color: #000000;
        float: right;
        font-size: 28px;
        font-weight: bold;
        cursor: pointer;
        line-height: 20px;
    }
    
    .close:hover {
        opacity: 0.7;
    }
    
    .modal-header {
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid #e5e5e5;
    }
    
    .modal-header h2 {
        margin: 0;
        color: #000000 !important;
        font-size: 1.5rem;
    }
    
    .creators-list {
        list-style: none;
        padding: 0;
        margin: 0;
    }
    
    .creators-list li {
        padding: 0.75rem 0;
        border-bottom: 1px solid #f0f0f0;
        color: #000000 !important;
        font-size: 1rem;
    }
    
    .creators-list li strong {
        color: #000000 !important;
    }
    
    .creators-list li:last-child {
        border-bottom: none;
    }
    
    /* Ensure all modal text is black */
    .modal-content, .modal-content *, .modal-content p, .modal-content div, .modal-content span {
        color: #000000 !important;
    }
    
    .close {
        color: #000000 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Define the model class
class VGG16DeepFake(nn.Module):
    def __init__(self):
        super(VGG16DeepFake, self).__init__()
        self.vgg16 = models.vgg16(pretrained=True)
        for param in self.vgg16.parameters():
            param.requires_grad = False
        self.vgg16.classifier = nn.Sequential(
            nn.Linear(25088, 512),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(512, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.vgg16(x)

# Load model
@st.cache_resource
def load_model(path='model_15.pth'):
    try:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model = VGG16DeepFake().to(device)
        
        # Download model from Google Drive if not exists
        if not os.path.exists(path):
            # Google Drive file ID - Replace with your actual file ID
            # To get file ID: Upload to Google Drive, right-click > Get link > Extract ID from URL
            GOOGLE_DRIVE_FILE_ID = "1_jvUsjViG56UqhxpPjBgSIAzzvQdUYX3"
            
            if GOOGLE_DRIVE_FILE_ID and GOOGLE_DRIVE_FILE_ID != "YOUR_GOOGLE_DRIVE_FILE_ID_HERE" and gdown:
                try:
                    with st.spinner("Downloading model file from Google Drive (this may take a few minutes)..."):
                        url = f'https://drive.google.com/uc?id={GOOGLE_DRIVE_FILE_ID}'
                        gdown.download(url, path, quiet=False)
                        st.success("Model downloaded successfully!")
                except Exception as e:
                    st.error(f"Failed to download model: {str(e)}")
                    return None, None
            else:
                st.error(f"""
                **Model file '{path}' not found.**
                
                Please upload the model file to Google Drive and update the GOOGLE_DRIVE_FILE_ID in app.py
                
                Or place the model file manually in the app directory.
                """)
                return None, None
        
        # Check if file is a Git LFS pointer (text file instead of binary)
        file_size = os.path.getsize(path)
        if file_size < 1000:  # Git LFS pointers are typically very small
            with open(path, 'r') as f:
                first_line = f.readline().strip()
                if first_line == "version https://git-lfs.github.com/spec/v1":
                    st.error("""
                    **Model file is a Git LFS pointer, not the actual model.**
                    
                    Please download the actual model file or update the Google Drive file ID.
                    """)
                    return None, None
            
        model.load_state_dict(torch.load(path, map_location=device, weights_only=False))
        model.eval()
        return model, device
    except Exception as e:
        error_msg = str(e)
        if "invalid load key" in error_msg.lower():
            st.error(f"""
            **Error loading model file.**
            
            The model file appears to be corrupted or is not a valid PyTorch model file.
            
            **Possible solutions:**
            1. Ensure you have the actual model file (should be ~110MB), not a Git LFS pointer
            2. Re-download the model file from the original source
            3. Train a new model using the `Train.ipynb` notebook
            
            **Error details:** {error_msg}
            """)
        else:
            st.error(f"Error loading model: {error_msg}")
        return None, None

# Preprocessing function
def preprocess_image(image):
    try:
        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225])
        ])
        image = image.convert("RGB")
        return transform(image).unsqueeze(0)
    except Exception as e:
        st.error(f"Error preprocessing image: {str(e)}")
        return None

# Sidebar
with st.sidebar:
    st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    st.markdown("**About**")
    st.markdown("""
    Uses a fine-tuned VGG16 model to detect synthetic and manipulated facial images.
    
    **Supported:** JPEG, PNG
    
    **Best results:** Clear, well-lit face images.
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    st.markdown("**Settings**")
    show_confidence = st.checkbox("Show confidence", value=True)
    show_details = st.checkbox("Technical details", value=False)
    st.markdown('</div>', unsafe_allow_html=True)

# About Creators Button and Modal - Place at the very top
st.markdown("""
    <div style="position: fixed; top: 1rem; right: 1rem; z-index: 1000;">
        <button id="creatorsBtn" style="background-color: #e5e7eb; color: #000000; border: 1px solid #9ca3af; padding: 0.5rem 1rem; border-radius: 6px; font-weight: 600; cursor: pointer; font-size: 0.9rem;">About Creators</button>
    </div>
    
    <!-- Modal -->
    <div id="creatorsModal" class="modal">
        <div class="modal-content">
            <span class="close" id="closeModal">&times;</span>
            <div class="modal-header">
                <h2 style="color: #000000 !important;">Project Creators</h2>
            </div>
            <ul class="creators-list">
                <li style="color: #000000 !important;"><strong style="color: #000000 !important;">Mrigankar Sonowal</strong> - MBA/BA04/015</li>
                <li style="color: #000000 !important;"><strong style="color: #000000 !important;">Rahul Kumar</strong> - MBA/BA04/031</li>
                <li style="color: #000000 !important;"><strong style="color: #000000 !important;">Shristi Singh</strong> - MBA/BA04/022</li>
                <li style="color: #000000 !important;"><strong style="color: #000000 !important;">Shubham Warkade</strong> - MBA/BA04/023</li>
                <li style="color: #000000 !important;"><strong style="color: #000000 !important;">Vala Jaydeep</strong> - MBA/BA04/030</li>
                <li style="color: #000000 !important;"><strong style="color: #000000 !important;">Abhishek Bahal</strong> - MBA/BA04/003</li>
            </ul>
        </div>
    </div>
    
    <script>
    (function() {
        var btn = document.getElementById('creatorsBtn');
        var modal = document.getElementById('creatorsModal');
        var closeBtn = document.getElementById('closeModal');
        
        if (btn) {
            btn.onclick = function() {
                if (modal) modal.style.display = 'block';
            };
        }
        
        if (closeBtn) {
            closeBtn.onclick = function() {
                if (modal) modal.style.display = 'none';
            };
        }
        
        // Close modal when clicking outside
        if (modal) {
            window.onclick = function(event) {
                if (event.target == modal) {
                    modal.style.display = 'none';
                }
            };
        }
        
        // Close with Escape key
        document.addEventListener('keydown', function(event) {
            if (event.key === 'Escape' && modal) {
                modal.style.display = 'none';
            }
        });
    })();
    </script>
""", unsafe_allow_html=True)

# Main content - compact header
st.markdown("""
    <div class="main-container">
        <div class="brand-header">
            <h1 class="brand-title">DeepFake Detector</h1>
            <p class="brand-subtitle">AI-powered image authenticity verification</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# File uploader - compact
st.markdown('<div class="main-container">', unsafe_allow_html=True)
uploaded_file = st.file_uploader(
    "Upload Image", 
    type=["jpg", "jpeg", "png"],
    help="Upload a JPG, JPEG, or PNG image containing a face"
)

if uploaded_file is not None:
    try:
        # Compact layout - side by side
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown('<div class="image-container">', unsafe_allow_html=True)
            image = Image.open(uploaded_file)
            st.image(image, width=None)
            if show_details:
                with st.expander("Details"):
                    st.write(f"Format: {image.format}")
                    st.write(f"Size: {image.size[0]} × {image.size[1]} px")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<p class="section-title">Results</p>', unsafe_allow_html=True)
            
            # Progress bar during processing
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Step 1: Loading model
            status_text.text("Loading model...")
            progress_bar.progress(25)
            model, device = load_model()
            
            if model is None or device is None:
                st.error("Failed to load model.")
            else:
                # Step 2: Preprocessing
                status_text.text("Preprocessing image...")
                progress_bar.progress(50)
                input_tensor = preprocess_image(image)
                
                if input_tensor is not None:
                    # Step 3: Processing
                    status_text.text("Analyzing image...")
                    progress_bar.progress(75)
                    input_tensor = input_tensor.to(device)
                    
                    with torch.no_grad():
                        output = model(input_tensor)
                        prob = output.item()
                        pred_label = "Real" if prob > 0.5 else "Fake"
                        confidence = prob if prob > 0.5 else (1 - prob)
                        confidence_pct = confidence * 100
                    
                    # Step 4: Complete
                    progress_bar.progress(100)
                    status_text.text("Analysis complete")
                    
                    # Display prediction
                    if pred_label == "Real":
                        st.markdown(f"""
                        <div class="prediction-card prediction-real">
                            <h2 class="prediction-label prediction-label-real">AUTHENTIC</h2>
                            <p class="prediction-desc">Image verified as authentic.</p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="prediction-card prediction-fake">
                            <h2 class="prediction-label prediction-label-fake">SYNTHETIC</h2>
                            <p class="prediction-desc">Image may contain synthetic content.</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Confidence score
                    if show_confidence:
                        st.markdown("""
                        <div class="confidence-section">
                            <div class="confidence-label">Confidence</div>
                        </div>
                        """, unsafe_allow_html=True)
                        st.progress(confidence)
                        st.markdown(f'<div class="confidence-value">{confidence_pct:.1f}%</div>', unsafe_allow_html=True)
                    
                    # Technical details
                    if show_details:
                        with st.expander("Technical Details"):
                            st.write(f"Probability: {prob:.6f}")
                            st.write(f"Threshold: 0.5")
                            st.write(f"Device: {device}")
                    
                    # Clear progress
                    progress_bar.empty()
                    status_text.empty()
        
        st.markdown('</div>', unsafe_allow_html=True)
                        
    except Exception as e:
        st.error(f"Error: {str(e)}")

else:
    st.markdown("""
    <div style="text-align: center; padding: 3rem;">
        <p style="color: #000000; font-size: 1rem;">Upload an image to begin analysis</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)