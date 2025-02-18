import cv2
import numpy as np
import pytesseract
import json
import random
import os
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import Response
from io import BytesIO

router = APIRouter()

def load_image(image_path):
    """Load image and convert to grayscale."""
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return image, gray

def preprocess_image(gray_image):
    """Apply adaptive thresholding & morphology to enhance structure."""
    blurred = cv2.GaussianBlur(gray_image, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY_INV, 11, 2)
    
    # Morphological operations to refine edges
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    processed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)
    
    return processed

def detect_elements(processed_image):
    """Find UI elements using contour detection."""
    contours, _ = cv2.findContours(processed_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours

def classify_ui_element(w, h, text):
    """Classify UI elements based on size and text presence."""
    if text:
        return "text"
    elif w > 150 and h < 60:
        return "button"
    elif w > 50 and h > 50:
        return "image"
    elif 50 < w < 150 and 10 < h < 50:
        return "input_field"
    return "unknown"

def extract_annotations(contours, gray_image):
    """Extract bounding boxes and classify UI elements."""
    annotations = []
    
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        
        if w > 25 and h > 25:  # Ignore very small detections
            roi = gray_image[y:y+h, x:x+w]
            text = pytesseract.image_to_string(roi, config='--psm 6').strip()
            element_type = classify_ui_element(w, h, text)
            
            annotations.append({"x": x, "y": y, "w": w, "h": h, "type": element_type, "text": text})
    
    return annotations

def augment_image(image, annotations):
    """Apply augmentation to UI screenshots for better model generalization."""
    height, width = image.shape[:2]

    # Random Rotation
    angle = random.randint(-10, 10)
    matrix = cv2.getRotationMatrix2D((width//2, height//2), angle, 1)
    rotated = cv2.warpAffine(image, matrix, (width, height))

    # Brightness & Contrast Adjustments
    alpha = random.uniform(0.8, 1.2)  # Contrast
    beta = random.randint(-30, 30)  # Brightness
    adjusted = cv2.convertScaleAbs(rotated, alpha=alpha, beta=beta)

    # Add Gaussian Noise
    noise = np.random.normal(0, 15, adjusted.shape).astype(np.uint8)
    noisy = cv2.add(adjusted, noise)

    # Random Blur
    if random.random() > 0.5:
        noisy = cv2.GaussianBlur(noisy, (5, 5), 0)

    # Recalculate Bounding Boxes
    new_annotations = []
    for ann in annotations:
        x, y, w, h = ann["x"], ann["y"], ann["w"], ann["h"]
        new_x = int(x + np.sin(np.radians(angle)) * h)
        new_y = int(y + np.sin(np.radians(angle)) * w)
        new_annotations.append({"x": new_x, "y": new_y, "w": w, "h": h, "type": ann["type"], "text": ann["text"]})
    
    return noisy, new_annotations

def save_annotations(annotations, filename):
    """Save annotations as JSON for model training."""
    with open(filename, "w") as f:
        json.dump(annotations, f, indent=4)

@router.post("/detect-elements/")
async def detect_ui_elements(file: UploadFile = File(...)):
    """
    API endpoint to detect UI elements using OpenCV contour detection.
    Accepts an image file and returns the processed image with bounding boxes.
    """
    # Read image file
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Preprocess image
    processed = preprocess_image(gray)

    # Detect elements & extract bounding boxes
    contours = detect_elements(processed)
    annotations = extract_annotations(contours, gray)

    # Augment the image with bounding boxes
    for ann in annotations:
        x, y, w, h = ann["x"], ann["y"], ann["w"], ann["h"]
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Drawing bounding boxes

    # Encode image to send as response
    _, encoded_img = cv2.imencode(".png", image)
    
    return Response(content=encoded_img.tobytes(), media_type="image/png")

# For image augmentation, you can use the augment_image function if required

