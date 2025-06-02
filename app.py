import streamlit as st
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import io

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
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = VGG16DeepFake().to(device)
    model.load_state_dict(torch.load(path, map_location=device))
    model.eval()
    return model, device

# Preprocessing function
def preprocess_image(image):
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225])
    ])
    image = image.convert("RGB")
    return transform(image).unsqueeze(0)

# Streamlit UI
st.title("DeepFake Face Detection App")
st.write("Upload an image to check if it's Real or Fake")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    # st.image(image, caption="Uploaded Image", use_container_width=True)
    st.image(image, caption="Uploaded Image", width=300)


    model, device = load_model()
    input_tensor = preprocess_image(image).to(device)

    with torch.no_grad():
        output = model(input_tensor)
        prob = output.item()
        pred_label = "Real" if prob > 0.5 else "Fake"

    # st.markdown(f"### Prediction: **{pred_label}** ({prob:.4f})")
    st.markdown(f"### Prediction: **{pred_label}**")