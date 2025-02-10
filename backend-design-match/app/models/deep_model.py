import torch
import torch.nn.functional as F
from torchvision import transforms
from PIL import Image
import numpy as np

class DeepModel:
    def __init__(self, model_path="app/models/ui_comparator.pth"):
        """Initialize the deep learning model."""
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = self.load_model(model_path)

    def load_model(self, model_path):
        """Load the pre-trained deep learning model."""
        model = torch.load(model_path, map_location=self.device)
        model.eval()
        return model

    def compare_images(self, figma_img, ui_img):
        """Compare UI images using deep learning."""
        with torch.no_grad():
            figma_tensor = self.preprocess(figma_img).to(self.device)
            ui_tensor = self.preprocess(ui_img).to(self.device)

            similarity_score = F.cosine_similarity(figma_tensor, ui_tensor).item()
            issues = self.detect_issues(similarity_score)

        return round(similarity_score * 100, 2), issues

    def preprocess(self, img):
        """Convert image to tensor for deep model."""
        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
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
