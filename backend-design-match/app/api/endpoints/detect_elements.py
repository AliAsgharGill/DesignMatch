import cv2
import numpy as np
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import Response

router = APIRouter()

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

    # Apply Edge Detection
    edges = cv2.Canny(gray, 50, 150)

    # Find Contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw Bounding Boxes
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if w > 30 and h > 30:  # Filter small elements
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Encode image to send as response
    _, encoded_img = cv2.imencode(".png", image)
    
    return Response(content=encoded_img.tobytes(), media_type="image/png")
