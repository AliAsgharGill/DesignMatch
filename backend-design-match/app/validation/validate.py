import os
import cv2
import tempfile
import base64
import numpy as np
import pytesseract
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse
from skimage.metrics import structural_similarity as ssim
from fuzzywuzzy import fuzz
from ultralytics import YOLO
from auth.dependencies import get_current_user

# Define YOLO model path
model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "model", "best_60k.pt"))

if not os.path.exists(model_path):
    raise FileNotFoundError(f"❌ Model file not found at: {os.path.abspath(model_path)}")

print(f"✅ Loading YOLO model from: {os.path.abspath(model_path)}")
model = YOLO(model_path)
print("🎯 Model loaded successfully!")

# Set Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"/usr/local/bin/tesseract"

router = APIRouter()

def detect_ui_elements(image):
    """Detect UI elements using YOLOv8 model."""
    results = model(image)
    elements = []
    for r in results:
        for box in r.boxes.data:
            x1, y1, x2, y2, conf, cls = box.tolist()
            elements.append({
                "label": r.names[int(cls)],
                "bbox": [int(x1), int(y1), int(x2), int(y2)],
                "confidence": round(conf * 100, 2),
            })
    return elements

def compare_elements(figma_elements, ui_elements):
    """Compare detected UI elements between Figma and implemented UI."""
    issues = []
    figma_labels = {el['label'] for el in figma_elements}
    ui_labels = {el['label'] for el in ui_elements}

    missing_elements = figma_labels - ui_labels
    extra_elements = ui_labels - figma_labels

    for el in missing_elements:
        issues.append({"type": "Missing Element", "description": f"{el} is missing in the UI"})
    for el in extra_elements:
        issues.append({"type": "Extra Element", "description": f"{el} is extra in the UI"})
    
    return issues

def extract_text(image):
    """Extract text from an image using Tesseract OCR with grayscale preprocessing."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)
    return text.strip()

def compare_text(figma_text, ui_text):
    """Compare extracted text from Figma and UI images using fuzzy logic."""
    similarity = fuzz.ratio(figma_text, ui_text)
    return similarity

def compute_ssim(figma_image, ui_image):
    """Compute Structural Similarity Index (SSIM) for layout comparison."""
    # Resize figma_image to match the dimensions of ui_image if necessary
    if figma_image.shape != ui_image.shape:
        figma_image = cv2.resize(figma_image, (ui_image.shape[1], ui_image.shape[0]))
    figma_gray = cv2.cvtColor(figma_image, cv2.COLOR_BGR2GRAY)
    ui_gray = cv2.cvtColor(ui_image, cv2.COLOR_BGR2GRAY)
    score, _ = ssim(figma_gray, ui_gray, full=True)
    return score


def detect_text_areas(image):
    """Detect text areas and return bounding boxes."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Invert binary thresholding to detect white text on dark background if needed
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    text_regions = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if h > 10:  # Filter out very small regions
            text_regions.append((x, y, w, h))
    return text_regions

@router.post("/validate/layout", dependencies=[Depends(get_current_user)])
async def validate_layout(figma_path: str, ui_path: str):
    # Read images
    figma_image = cv2.imread(figma_path)
    ui_image = cv2.imread(ui_path)
    
    if figma_image is None or ui_image is None:
        raise HTTPException(status_code=400, detail="Invalid image paths")

    # UI Element Detection using YOLOv8
    figma_elements = detect_ui_elements(figma_image)
    ui_elements = detect_ui_elements(ui_image)
    element_issues = compare_elements(figma_elements, ui_elements)

    # Text Extraction & Comparison
    figma_text = extract_text(figma_image)
    ui_text = extract_text(ui_image)
    text_similarity = compare_text(figma_text, ui_text)

    # Layout similarity using SSIM
    layout_similarity = compute_ssim(figma_image, ui_image)

    # Detect text areas for alignment validation
    figma_text_areas = detect_text_areas(figma_image)
    ui_text_areas = detect_text_areas(ui_image)

    # Visual Issue Highlighting: Copy Figma image to draw highlights
    highlighted_image = figma_image.copy()
    text_alignment_issues = []
    threshold = 20  # pixels tolerance for alignment

    # For each text area in the Figma image, look for a matching region in the UI image
    for i, (fx, fy, fw, fh) in enumerate(figma_text_areas):
        matching = any(
            abs(fx - ux) < threshold and abs(fy - uy) < threshold
            for (ux, uy, uw, uh) in ui_text_areas
        )
        if not matching:
            # Mark missing/misaligned text in red
            cv2.rectangle(highlighted_image, (fx, fy), (fx + fw, fy + fh), (0, 0, 255), 2)
            text_alignment_issues.append({
                "type": "Text Alignment",
                "description": f"Text region at ({fx}, {fy}, {fw}, {fh}) is misaligned or missing."
            })

    # Draw green boxes for text areas detected in the UI image for reference
    for (ux, uy, uw, uh) in ui_text_areas:
        cv2.rectangle(highlighted_image, (ux, uy), (ux + uw, uy + uh), (0, 255, 0), 2)

    # Compute an overall match score (weighted average: layout 60% and text 40%)
    overall_match_score = round((layout_similarity * 100 * 0.6) + (text_similarity * 0.4), 2)

    # Combine all issues
    issues = element_issues.copy()
    if text_similarity < 90:
        issues.append({
            "type": "Text Similarity",
            "description": f"Text similarity is {text_similarity}%, which is below the acceptable threshold."
        })
    issues.extend(text_alignment_issues)
    issues.append({
        "type": "Layout Similarity",
        "description": f"Layout similarity score (SSIM): {layout_similarity:.2f}"
    })

    # Encode highlighted image as base64 to embed in HTML report
    _, buffer = cv2.imencode(".png", highlighted_image)
    img_base64 = base64.b64encode(buffer).decode("utf-8")

    # Generate detailed HTML report
    result_html = f"""
    <html>
        <head>
            <title>UI Validation Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                table {{ width: 90%; margin: auto; border-collapse: collapse; }}
                th, td {{ padding: 10px; text-align: left; border: 1px solid #ddd; }}
                th {{ background-color: #f4f4f4; }}
                .issue-table {{ margin-top: 20px; }}
                .score {{ font-size: 1.2em; }}
                img {{ display: block; margin: auto; width: 70%; border: 3px solid #333; }}
            </style>
        </head>
        <body>
            <h1>UI Validation Results</h1>
            <h2 class="score">Overall Match Score: {overall_match_score}%</h2>
            <h3>Layout Similarity (SSIM): {layout_similarity:.2f}</h3>
            <h3>Text Similarity: {text_similarity}%</h3>
            <h2>Issues Detected:</h2>
            <table class="issue-table">
                <tr><th>Issue Type</th><th>Description</th></tr>
                {''.join(f'<tr><td>{issue["type"]}</td><td>{issue["description"]}</td></tr>' for issue in issues)}
            </table>
            <h2>Visual Highlighting:</h2>
            <p>Red boxes indicate missing/misaligned text regions in the UI compared to the Figma design. Green boxes mark detected text areas in the UI.</p>
            <img src="data:image/png;base64,{img_base64}" alt="Highlighted UI Validation">
        </body>
    </html>
    """

    # Write HTML report to a temporary file
    temp_dir = tempfile.gettempdir()
    html_file_path = os.path.join(temp_dir, "ui_validation_report.html")
    with open(html_file_path, "w", encoding="utf-8") as html_file:
        html_file.write(result_html)

    return {"issues": issues, "overall_match_score": overall_match_score, "html_report_url": "/validate/layout/download"}

@router.get("/validate/layout/download", dependencies=[Depends(get_current_user)])
async def download_report():
    """Download the generated UI validation report."""
    temp_dir = tempfile.gettempdir()
    html_file_path = os.path.join(temp_dir, "ui_validation_report.html")
    
    if not os.path.exists(html_file_path):
        raise HTTPException(status_code=404, detail="Report not found")
    
    return FileResponse(html_file_path, media_type="text/html", filename="ui_validation_report.html")
