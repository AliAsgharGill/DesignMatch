import shutil
from pathlib import Path

from fastapi import UploadFile

temp_dir = Path("temp")
temp_dir.mkdir(parents=True, exist_ok=True)


def save_upload_file(upload_file: UploadFile, destination: Path) -> str:
    with destination.open("wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    return str(destination)
