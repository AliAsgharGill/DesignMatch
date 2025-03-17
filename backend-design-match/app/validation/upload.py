from datetime import datetime
from pathlib import Path
from typing import Literal

from fastapi import APIRouter, File, HTTPException, UploadFile, status, Depends

from utils.file_handler import save_upload_file

from auth.dependencies import get_current_user

router = APIRouter()

ALLOWED_CONTENT_TYPES = {"image/png", "image/jpeg"}


def validate_image_file(file: UploadFile) -> None:
    """Validate if the uploaded file is an allowed image type."""
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"File type not allowed. Allowed types: {', '.join(ALLOWED_CONTENT_TYPES)}",
        )


async def process_upload(
    file: UploadFile, upload_type: Literal["figma", "ui"]
) -> dict[str, str]:
    """
    Process file upload for both figma and ui endpoints.

    Args:
        file: The uploaded file
        upload_type: Type of upload ('figma' or 'ui')

    Returns:
        Dictionary containing the saved file path
    """
    validate_image_file(file)

    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        original_name = Path(file.filename).stem
        extension = Path(file.filename).suffix
        file_name = f"{upload_type}_{original_name}_{timestamp}{extension}"

        file_path = await save_upload_file(file, Path("temp") / file_name)
        return {"file_path": str(file_path)}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing file upload: {str(e)}",
        ) from e


@router.post("/upload/figma", status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_current_user)])
async def upload_figma(file: UploadFile = File(...)) -> dict[str, str]:
    """
    Handle Figma file uploads.

    Args:
        file: The uploaded image file (PNG or JPEG)

    Returns:
        Dictionary containing the saved file path
    """
    return await process_upload(file, "figma")


@router.post("/upload/ui", status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_current_user)])
async def upload_ui(file: UploadFile = File(...)) -> dict[str, str]:
    """
    Handle UI file uploads.

    Args:
        file: The uploaded image file (PNG or JPEG)

    Returns:
        Dictionary containing the saved file path
    """
    return await process_upload(file, "ui")
