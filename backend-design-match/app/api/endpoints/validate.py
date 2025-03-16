import base64
import os
import tempfile

import cv2
import numpy as np
import pytesseract
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from fuzzywuzzy import fuzz
from skimage.metrics import structural_similarity as ssim

# pytesseract path
pytesseract.pytesseract.tesseract_cmd = r"/usr/local/bin/tesseract"


router = APIRouter()


def compare_text(figma_text, ui_text):
    """Compare extracted text using fuzzy logic to allow minor variations."""
    similarity_score = fuzz.ratio(figma_text.lower(), ui_text.lower())
    return similarity_score, similarity_score >= 80


def design_match_score(figma_img, ui_img):
    """Calculate Structural Similarity Index (SSIM) to compare UI and Figma layouts."""
    figma_gray = cv2.cvtColor(figma_img, cv2.COLOR_BGR2GRAY)
    ui_gray = cv2.cvtColor(ui_img, cv2.COLOR_BGR2GRAY)

    # Resize Figma image to UI size to align dimensions
    figma_resized = cv2.resize(figma_gray, (ui_gray.shape[1], ui_gray.shape[0]))

    # Compute Structural Similarity Index (SSIM)
    similarity_index, _ = ssim(figma_resized, ui_gray, full=True)

    return round(similarity_index * 100, 2)


def detect_text_areas(image):
    """Detect text areas and return bounding boxes."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    text_regions = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if h > 10:  # Ignore small elements
            text_regions.append((x, y, w, h))
    return text_regions


@router.post("/validate/layout")
async def validate_layout(figma_path: str, ui_path: str):
    figma_image = cv2.imread(figma_path)
    ui_image = cv2.imread(ui_path)

    if figma_image is None or ui_image is None:
        raise HTTPException(status_code=400, detail="Invalid image paths")

    # Resize figma image to UI dimensions
    figma_resized = cv2.resize(figma_image, (ui_image.shape[1], ui_image.shape[0]))

    # Compute Design Match Score using SSIM
    design_score = design_match_score(figma_resized, ui_image)

    # Extract and compare text
    text_figma = pytesseract.image_to_string(figma_resized).strip()
    text_ui = pytesseract.image_to_string(ui_image).strip()
    text_similarity, text_matched = compare_text(text_figma, text_ui)

    # Detect text areas for alignment validation
    figma_text_areas = detect_text_areas(figma_resized)
    ui_text_areas = detect_text_areas(ui_image)

    # Highlight mismatches
    highlighted_image = figma_resized.copy()
    issues = []

    for i, (fx, fy, fw, fh) in enumerate(figma_text_areas):
        matching = any(
            abs(fx - ux) < 20 and abs(fy - uy) < 20
            for (ux, uy, uw, uh) in ui_text_areas
        )
        if not matching:
            # Mark missing/misplaced text in Red (Critical)
            cv2.rectangle(
                highlighted_image, (fx, fy), (fx + fw, fy + fh), (0, 0, 255), 2
            )
            issues.append(
                {
                    "id": i + 1,
                    "type": "Critical",
                    "description": "Text missing or misplaced",
                }
            )

    # Draw reference boxes for UI-detected text (Green for matched)
    for ux, uy, uw, uh in ui_text_areas:
        cv2.rectangle(highlighted_image, (ux, uy), (ux + uw, uy + uh), (0, 255, 0), 2)

    # Overall UI Match Score (Weighted average of Text & Design Scores)
    overall_match_score = round((design_score * 0.6) + (text_similarity * 0.4), 2)

    _, buffer = cv2.imencode(".png", highlighted_image)
    img_base64 = base64.b64encode(buffer).decode("utf-8")

    # Generate issue report
    issue_report = "".join(
        f'<tr class="{issue["type"].lower()}"><td>{issue["id"]}</td><td>{issue["type"]}</td><td>{issue["description"]}</td></tr>'
        for issue in issues
    )

    result_html = f"""
    <html>
        <head>
            <title>UI Validation Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                table {{ width: 90%; margin: auto; border-collapse: collapse; }}
                th, td {{ padding: 10px; text-align: left; border: 1px solid #ddd; }}
                th {{ background-color: #f4f4f4; }}
                .critical {{ background-color: #ffcccc; }}
                img {{ display: block; margin: auto; width: 70%; border: 3px solid black; }}
            </style>
        </head>
        <body>
            <h1>UI Validation Results</h1>
            <h3>🎨 **Design Match Score**: {design_score}%</h3>
            <h3>📝 **Text Match Score**: {text_similarity}% ({'✔️ Matched' if text_matched else '❌ Mismatch'})</h3>
            <h2>📊 **Overall Match Score**: {overall_match_score}%</h2>

            <h2>Issues Detected:</h2>
            <table>
                <tr><th>#</th><th>Issue Type</th><th>Description</th></tr>
                {issue_report}
            </table>

            <h3>Highlighted Image:</h3>
            <img src="data:image/png;base64,{img_base64}" alt="Highlighted Image">
        </body>
    </html>
    """

    temp_dir = tempfile.gettempdir()
    html_file_path = os.path.join(temp_dir, "ui_validation_report.html")
    with open(html_file_path, "w", encoding="utf-8") as html_file:
        html_file.write(result_html)

    # JSON response with validation results
    response_data = {
        "design_match_score": design_score,
        "text_match_score": text_similarity,
        "overall_match_score": overall_match_score,
        "issues": issues,
        "html_report_url": "/validate/layout/download",
    }

    return response_data


@router.get("/validate/layout/download")
async def download_report():
    """Download the generated UI validation report."""
    temp_dir = tempfile.gettempdir()
    html_file_path = os.path.join(temp_dir, "ui_validation_report.html")

    if not os.path.exists(html_file_path):
        raise HTTPException(status_code=404, detail="Report not found")

    return FileResponse(
        html_file_path, media_type="text/html", filename="ui_validation_report.html"
    )
