import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import numpy as np

class DeepModel:
    def __init__(self, model_path=None):
        """Initialize the deep learning model."""
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = self.load_model(model_path)
        self.model.to(self.device)
        self.model.eval()

    def load_model(self, model_path):
        """Load a pre-trained model (ResNet50) or a custom model if provided."""
        if model_path:
            model = torch.load(model_path, map_location=self.device)
        else:
            model = models.resnet50(pretrained=True)
            model = nn.Sequential(*list(model.children())[:-1])  # Remove last FC layer

        return model

    def compare_images(self, figma_img, ui_img):
        """Compare UI images using deep learning."""
        with torch.no_grad():
            figma_tensor = self.preprocess(figma_img).to(self.device)
            ui_tensor = self.preprocess(ui_img).to(self.device)

            figma_features = self.model(figma_tensor).squeeze()
            ui_features = self.model(ui_tensor).squeeze()

            similarity_score = F.cosine_similarity(figma_features, ui_features, dim=0).item()
            issues = self.detect_issues(similarity_score)

        return round(similarity_score * 100, 2), issues

    def preprocess(self, img):
        """Convert image to tensor for deep model."""
        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),  # Standard normalization
        ])
        img = Image.fromarray(img)
        return transform(img).unsqueeze(0)

    def detect_issues(self, score):
        """Detect potential UI issues based on similarity score."""
        if score < 0.7:
            return ["Significant UI mismatch detected."]
        elif score < 0.9:
            return ["Minor UI inconsistencies found."]
        else:
            return ["UI matches design with high confidence."]
