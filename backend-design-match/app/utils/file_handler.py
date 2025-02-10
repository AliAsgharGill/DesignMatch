import shutil
from pathlib import Path

from fastapi import UploadFile

temp_dir = Path("temp")
temp_dir.mkdir(parents=True, exist_ok=True)


async def save_upload_file(file: UploadFile, destination: Path) -> Path:
    """
    Save an uploaded file to the specified destination.

    Args:
        file: The uploaded file
        destination: Path where the file should be saved

    Returns:
        Path to the saved file
    """
    destination.parent.mkdir(parents=True, exist_ok=True)

    content = await file.read()
    with open(destination, "wb") as f:
        f.write(content)

    return destination
