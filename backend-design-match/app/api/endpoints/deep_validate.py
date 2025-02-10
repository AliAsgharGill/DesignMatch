from fastapi import APIRouter, HTTPException
import cv2
import numpy as np
from services.deep_ui_comparison import validate_using_deep_model

router = APIRouter()

@router.post("/validate/deep")
async def validate_deep(figma_path: str, ui_path: str):

    """Validate UI using deep learning-based comparison."""
    figma_image = cv2.imread(figma_path)
    ui_image = cv2.imread(ui_path)

    if figma_image is None or ui_image is None:
        raise HTTPException(status_code=400, detail="Invalid image paths")
    
    match_score, issues = validate_using_deep_model(figma_image, ui_image)
    
    return {
        "deep_match_score": match_score,
        "issues": issues,
    }
