import torch
import torchvision.models as models

def load_deep_model():
    """Load a pre-trained deep learning model for UI comparison."""
    model = models.resnet18(pretrained=True)
    model.eval()  # Set model to evaluation mode
    return model
