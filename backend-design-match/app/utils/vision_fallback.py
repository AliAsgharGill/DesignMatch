# utils/vision_fallback.py

import cv2
from google.cloud import vision


def google_ocr_extract(image):
    """Use Google Cloud Vision API to extract text from an image."""
    try:
        client = vision.ImageAnnotatorClient()
        success, encoded_image = cv2.imencode(".png", image)

        if not success:
            raise ValueError("Failed to encode image for Google Vision.")

        content = encoded_image.tobytes()
        image = vision.Image(content=content)

        response = client.text_detection(image=image)
        annotations = response.text_annotations

        if response.error.message:
            raise RuntimeError(response.error.message)

        if annotations:
            return annotations[0].description.strip()

        return ""

    except Exception as e:
        print(f"❌ Google Vision OCR error: {e}")
        return ""
