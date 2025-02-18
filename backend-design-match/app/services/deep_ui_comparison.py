import cv2
import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image
from utils.model_loader import load_deep_model
from torchvision import transforms

# Load the deep learning model
model = load_deep_model()
model.eval()  # Ensure model is in evaluation mode

def preprocess_image(image):
    """Preprocess image for deep model."""
    transform = transforms.Compose([
        transforms.ToPILImage(),
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    return transform(image).unsqueeze(0)  # Add batch dimension

def validate_using_deep_model(figma_image, ui_image):
    """Compare UI with Figma design using a deep learning model."""
    # Convert images from BGR (OpenCV) to RGB
    figma_image = cv2.cvtColor(figma_image, cv2.COLOR_BGR2RGB)
    ui_image = cv2.cvtColor(ui_image, cv2.COLOR_BGR2RGB)

    # Preprocess images
    figma_tensor = preprocess_image(figma_image).to(torch.device("cuda" if torch.cuda.is_available() else "cpu"))
    ui_tensor = preprocess_image(ui_image).to(torch.device("cuda" if torch.cuda.is_available() else "cpu"))

    # Extract features using the model
    with torch.no_grad():
        figma_features = model(figma_tensor).squeeze()  # Remove batch dim
        ui_features = model(ui_tensor).squeeze()

    # Compute similarity (Cosine Similarity)
    similarity = F.cosine_similarity(figma_features, ui_features, dim=0).item()
    
    match_score = round(similarity * 100, 2)
    issues = []

    # Define issue detection thresholds
    if match_score < 70:
        issues.append({"type": "Critical Mismatch", "description": "Significant UI deviation from the design."})
    elif match_score < 85:
        issues.append({"type": "Minor Inconsistencies", "description": "Some minor UI mismatches detected."})

    return match_score, issues
