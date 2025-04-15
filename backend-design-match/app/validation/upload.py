import io
from datetime import datetime
from pathlib import Path
from typing import Literal

from auth.dependencies import get_current_user
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from PIL import Image
from utils.file_handler import save_upload_file
from utils.pdf_utils import pdf_to_images  # 🆕 You'll create this file

router = APIRouter()

ALLOWED_CONTENT_TYPES = {
    "image/png",
    "image/jpeg",
    "application/pdf",  # 🆕 Allow PDFs
}


def validate_file_type(file: UploadFile) -> None:
    """Validate if the uploaded file is an allowed image or PDF."""
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"File type not allowed. Allowed types: {', '.join(ALLOWED_CONTENT_TYPES)}",
        )


async def process_upload(file: UploadFile, upload_type: Literal["figma", "ui"]) -> dict:
    validate_file_type(file)
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        original_name = Path(file.filename).stem
        extension = Path(file.filename).suffix.lower()

        if extension == ".pdf":
            contents = await file.read()
            images = pdf_to_images(contents)
            paths = []

            for idx, img in enumerate(images):
                file_name = f"{upload_type}_{original_name}_{timestamp}_{idx}.png"
                path = Path("temp") / file_name
                img.save(path)
                paths.append(str(path))

            return {"file_paths": paths, "pages": len(paths)}

        else:
            file_name = f"{upload_type}_{original_name}_{timestamp}{extension}"
            file_path = await save_upload_file(file, Path("temp") / file_name)
            return {"file_path": str(file_path)}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing file upload: {str(e)}",
        ) from e


@router.post(
    "/upload/figma",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_user)],
)
async def upload_figma(file: UploadFile = File(...)) -> dict:
    return await process_upload(file, "figma")


@router.post(
    "/upload/ui",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_user)],
)
async def upload_ui(file: UploadFile = File(...)) -> dict:
    return await process_upload(file, "ui")


@router.post(
    "/upload/batch",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_user)],
)
async def upload_batch(files: list[UploadFile] = File(...)) -> dict:
    """Handles multiple image uploads at once for screen flows"""
    results = []
    for file in files:
        try:
            result = await process_upload(file, "batch")
            results.append(result)
        except Exception as e:
            results.append({"error": str(e), "filename": file.filename})
    return {"results": results}
