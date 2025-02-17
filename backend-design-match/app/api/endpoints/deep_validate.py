from fastapi import APIRouter, HTTPException
import cv2
import os
import logging
from services.deep_ui_comparison import validate_using_deep_model

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/validate/deep")
async def validate_deep(figma_path: str, ui_path: str):
    """Validate UI using deep learning-based comparison."""
    
    # Validate if file paths exist
    if not os.path.exists(figma_path) or not os.path.exists(ui_path):
        logger.error(f"Invalid file path(s): {figma_path}, {ui_path}")
        raise HTTPException(status_code=400, detail="One or both image paths are invalid or do not exist.")
    
    # Load images using OpenCV
    figma_image = cv2.imread(figma_path)
    ui_image = cv2.imread(ui_path)

    # Ensure images are properly loaded
    if figma_image is None or ui_image is None:
        logger.error(f"Failed to read images: {figma_path}, {ui_path}")
        raise HTTPException(status_code=400, detail="Error reading image files. Ensure they are valid image formats.")
    
    # Perform deep learning-based validation
    match_score, issues = validate_using_deep_model(figma_image, ui_image)
    
    return {
        "deep_match_score": match_score,
        "issues": issues,
    }
