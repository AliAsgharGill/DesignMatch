import base64
import os
import tempfile

import cv2
import numpy as np
import pytesseract
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

router = APIRouter()


def calculate_ssim(imageA, imageB):
    score = np.mean(np.abs(imageA - imageB))
    return 1 - (score / 255)


def compare_color(img1, img2):
    hist1 = cv2.calcHist([img1], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
    hist2 = cv2.calcHist([img2], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
    correlation = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
    return correlation


def detect_text(img):
    return pytesseract.image_to_string(img).strip()


# Issue categorization based on severity and specific mismatch types
def categorize_issue(
    area_size: int,
    text_diff: bool,
    color_diff: float,
    width_diff: float,
    element_type: str,
):
    if area_size > 1000 or text_diff:
        return "Critical", f"Element {element_type} text is not matching"
    elif area_size > 500 or color_diff < 0.9:
        return "Moderate", f"Element {element_type} color mismatch"
    elif width_diff > 20:  # Width mismatch detected
        return "Low Priority", f"Element {element_type} width is not accurate"
    else:
        return "Low Priority", f"Element {element_type} looks fine"


@router.post("/validate/layout")
async def validate_layout(figma_path: str, ui_path: str):
    figma_image = cv2.imread(figma_path)
    ui_image = cv2.imread(ui_path)

    if figma_image is None or ui_image is None:
        raise HTTPException(status_code=400, detail="Invalid image paths")

    figma_resized = cv2.resize(figma_image, (ui_image.shape[1], ui_image.shape[0]))

    similarity = calculate_ssim(figma_resized, ui_image)
    color_correlation = compare_color(figma_resized, ui_image)
    text_figma = detect_text(figma_resized)
    text_ui = detect_text(ui_image)

    diff = cv2.absdiff(figma_resized, ui_image)
    _, diff_thresh = cv2.threshold(
        cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY), 50, 255, cv2.THRESH_BINARY
    )
    contours, _ = cv2.findContours(
        diff_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    highlighted_image = figma_resized.copy()
    issues = []  # To store issue details

    for i, contour in enumerate(contours):
        if cv2.contourArea(contour) > 500:
            x, y, w, h = cv2.boundingRect(contour)
            # Check for width difference (simulating this as a placeholder, adjust logic as needed)
            width_diff = abs(
                w - figma_resized.shape[1] // len(contours)
            )  # Placeholder for width mismatch logic
            issue_type, description = categorize_issue(
                cv2.contourArea(contour),
                text_figma != text_ui,
                color_correlation,
                width_diff,
                "Element",
            )
            cv2.rectangle(highlighted_image, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(
                highlighted_image,
                f"{i+1}",
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 0, 255),
                2,
            )

            # Append issue details for the report
            issues.append({"id": i + 1, "type": issue_type, "description": description})

    # Generate report and add issue descriptions
    issue_report = ""
    for issue in issues:
        issue_report += f"<tr><td>{issue['id']}</td><td>{issue['type']}</td><td>{issue['description']}</td></tr>"

    # Encode highlighted_image to base64 string
    _, buffer = cv2.imencode(".png", highlighted_image)
    img_base64 = base64.b64encode(buffer).decode("utf-8")

    result_html = f"""
    <html>
        <head><title>UI Validation Report</title></head>
        <body>
            <h1>UI Validation Results</h1>
            <h3>Similarity Score: {round(similarity * 100, 2)}%</h3>
            <h3>Color Correlation: {color_correlation}</h3>
            <h2>Issues Detected:</h2>
            <table border="1">
                <tr><th>#</th><th>Issue Type</th><th>Description</th></tr>
                {issue_report}
            </table>
            <h3>Highlighted Image:</h3>
            <img src="data:image/png;base64,{img_base64}" alt="Highlighted Image">
        </body>
    </html>
    """

    # Save the HTML report in a temporary folder
    temp_dir = tempfile.gettempdir()
    html_file_path = os.path.join(temp_dir, "ui_validation_report.html")
    with open(html_file_path, "w", encoding="utf-8") as html_file:
        html_file.write(result_html)

    # Return the HTML report file as a downloadable response
    return FileResponse(
        html_file_path, media_type="text/html", filename="ui_validation_report.html"
    )


# pytesseract path
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
