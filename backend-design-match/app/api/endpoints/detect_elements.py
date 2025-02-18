import cv2
import numpy as np
import pytesseract
import json
import random
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import Response

router = APIRouter()

COLOR_MAPPING = {
    'image': (0, 255, 0),         # Green
    'button': (255, 0, 0),        # Blue
    'text': (0, 0, 255),          # Red
    'decorative': (0, 255, 255),  # Yellow
    'input_field': (255, 165, 0), # Orange
    'unknown': (200, 200, 200)    # Gray
}


def preprocess_image(gray_image):
    blurred = cv2.GaussianBlur(gray_image, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY_INV, 11, 2)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    processed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)
    return processed


def detect_elements(processed_image):
    contours, _ = cv2.findContours(processed_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours


def classify_ui_element(w, h, text):
    if text.strip():
        return 'text'
    elif w > 150 and h < 60:
        return 'button'
    elif w > 50 and h > 50:
        return 'image'
    elif 50 < w < 150 and 10 < h < 50:
        return 'input_field'
    elif w < 30 and h < 30:  # Small elements, could be icons
        return 'decorative'
    return 'unknown'


def extract_annotations(contours, gray_image):
    annotations = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if w < 10 or h < 10:  # Ignore tiny elements
            continue

        roi = gray_image[y:y + h, x:x + w]
        text = pytesseract.image_to_string(roi, config='--psm 6').strip()
        element_type = classify_ui_element(w, h, text)

        if not any(is_overlapping((x, y, w, h), ann) for ann in annotations):
            annotations.append({'x': x, 'y': y, 'w': w, 'h': h, 'type': element_type, 'text': text})

    return annotations


def is_overlapping(box1, ann):
    x1, y1, w1, h1 = box1
    x2, y2, w2, h2 = ann['x'], ann['y'], ann['w'], ann['h']

    return not (x1 + w1 < x2 or x2 + w2 < x1 or y1 + h1 < y2 or y2 + h2 < y1)


def draw_bounding_boxes(image, annotations):
    for ann in annotations:
        x, y, w, h, element_type = ann['x'], ann['y'], ann['w'], ann['h'], ann['type']
        color = COLOR_MAPPING.get(element_type, (200, 200, 200))
        cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)


@router.post("/detect-elements/")
async def detect_ui_elements(file: UploadFile = File(...)):
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    processed = preprocess_image(gray)
    contours = detect_elements(processed)
    annotations = extract_annotations(contours, gray)
    draw_bounding_boxes(image, annotations)

    _, encoded_img = cv2.imencode(".png", image)
    return Response(content=encoded_img.tobytes(), media_type="image/png")
