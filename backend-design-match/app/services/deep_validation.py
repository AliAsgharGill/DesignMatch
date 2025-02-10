import cv2
import numpy as np
from app.models.deep_model import DeepModel
from app.utils.deep_image_processing import preprocess_images

# Load the pre-trained model
deep_model = DeepModel()

def validate_using_deep_model(figma_image, ui_image):
    """Validate UI using a deep learning model."""

    # Preprocess images
    figma_processed, ui_processed = preprocess_images(figma_image, ui_image)

    # Get similarity score from deep model
    match_score, issues = deep_model.compare_images(figma_processed, ui_processed)

    return match_score, issues
