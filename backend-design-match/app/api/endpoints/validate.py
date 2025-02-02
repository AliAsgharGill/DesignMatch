import cv2
import numpy as np
from fastapi import APIRouter, HTTPException

router = APIRouter()


def calculate_ssim(imageA, imageB):
    score = np.mean(np.abs(imageA - imageB))
    return 1 - (score / 255)


def compare_color(img1, img2):
    # Convert to RGB from Grayscale to RGB for color-based comparison (if applicable)
    img1_rgb = cv2.cvtColor(img1, cv2.COLOR_GRAY2BGR)
    img2_rgb = cv2.cvtColor(img2, cv2.COLOR_GRAY2BGR)

    # Compute histogram comparison (could use other methods like Mean Squared Error or SSIM)
    hist1 = cv2.calcHist(
        [img1_rgb], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256]
    )
    hist2 = cv2.calcHist(
        [img2_rgb], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256]
    )

    # Compare histograms using correlation (other metrics are possible)
    correlation = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
    return correlation


@router.post("/validate/layout")
async def validate_layout(figma_path: str, ui_path: str):
    figma_image = cv2.imread(figma_path, cv2.IMREAD_GRAYSCALE)
    ui_image = cv2.imread(ui_path, cv2.IMREAD_GRAYSCALE)

    if figma_image is None or ui_image is None:
        raise HTTPException(status_code=400, detail="Invalid image paths")

    # Resize Figma image to match UI image size
    figma_resized = cv2.resize(figma_image, (ui_image.shape[1], ui_image.shape[0]))

    # Calculate SSIM to get overall similarity score
    similarity = calculate_ssim(figma_resized, ui_image)

    # Compare colors
    color_correlation = compare_color(figma_resized, ui_image)

    # Use a more relaxed difference threshold for layout
    diff = cv2.absdiff(figma_resized, ui_image)
    _, diff_thresh = cv2.threshold(diff, 50, 255, cv2.THRESH_BINARY)

    # Find contours (larger mismatches)
    contours, _ = cv2.findContours(
        diff_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    # Highlight the areas with significant mismatches (larger areas of difference)
    highlighted_image = cv2.cvtColor(
        figma_resized, cv2.COLOR_GRAY2BGR
    )  # Convert to BGR for color rectangles
    for contour in contours:
        if (
            cv2.contourArea(contour) > 500
        ):  # Ignore very small differences (larger area threshold)
            (x, y, w, h) = cv2.boundingRect(contour)

            # Optionally, check the width, height, padding, margin between elements
            if w != h:  # Example of width-height mismatch detection
                cv2.rectangle(highlighted_image, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.putText(
                    highlighted_image,
                    f"Width: {w}",
                    (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 0, 255),
                    2,
                )
            else:
                cv2.rectangle(
                    highlighted_image, (x, y), (x + w, y + h), (0, 255, 0), 2
                )  # Green rectangle for shape matches
                cv2.putText(
                    highlighted_image,
                    f"Height: {h}",
                    (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 0),
                    2,
                )

    # Optionally, save the result image or return the image
    result_path = "highlighted_result.png"
    cv2.imwrite(result_path, highlighted_image)

    return {
        "similarity_score": round(similarity * 100, 2),
        "color_correlation": color_correlation,
        "result_image_path": result_path,  # Provide the path to the highlighted image
    }
