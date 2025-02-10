import cv2
import numpy as np
import torch
from torchvision import transforms
from PIL import Image
from utils.model_loader import load_deep_model

# Load the deep learning model
model = load_deep_model()

def preprocess_image(image):

    """Preprocess image for deep model."""
    transform = transforms.Compose([
        transforms.ToPILImage(),
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    return transform(image).unsqueeze(0)

def validate_using_deep_model(figma_image, ui_image):
    """Compare UI with Figma design using a deep learning model."""
    figma_image = cv2.cvtColor(figma_image, cv2.COLOR_BGR2RGB)
    ui_image = cv2.cvtColor(ui_image, cv2.COLOR_BGR2RGB)

    figma_tensor = preprocess_image(figma_image)
    ui_tensor = preprocess_image(ui_image)

    # Pass through model
    with torch.no_grad():
        figma_features = model(figma_tensor)
        ui_features = model(ui_tensor)

    # Compute similarity (Cosine Similarity)
    similarity = torch.nn.functional.cosine_similarity(figma_features, ui_features).item()
    
    match_score = round(similarity * 100, 2)
    issues = []

    # Example: If similarity is below 85%, flag it as an issue
    if match_score < 85:
        issues.append({"type": "Mismatch", "description": "UI does not match the design accurately."})

    return match_score, issues
