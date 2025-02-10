import cv2
import numpy as np

def preprocess_images(figma_img, ui_img):
    """Preprocess images before feeding them into the deep model."""
    
    # Convert to grayscale
    figma_gray = cv2.cvtColor(figma_img, cv2.COLOR_BGR2GRAY)
    ui_gray = cv2.cvtColor(ui_img, cv2.COLOR_BGR2GRAY)

    # Resize images to the same dimension
    figma_resized = cv2.resize(figma_gray, (224, 224))
    ui_resized = cv2.resize(ui_gray, (224, 224))

    return figma_resized, ui_resized
