from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
from pathlib import Path
import uuid

router = APIRouter()

# ✅ BASE DIRECTORY (backend/app → backend)
BASE_DIR = Path(__file__).resolve().parent.parent

# ✅ ABSOLUTE UPLOAD PATH (same as convert.py)
UPLOAD_DIR = BASE_DIR / "uploads" / "input"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


class TextUpload(BaseModel):
    text: str


@router.post("/upload/text")
def upload_text(data: TextUpload):
    file_id = str(uuid.uuid4())
    file_path = UPLOAD_DIR / f"{file_id}.txt"

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(data.text)

    return {
        "status": "ok",
        "file_id": file_id,
        "file_path": str(file_path)
    }


@router.post("/upload/handwritten")
def upload_handwritten(file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())
    extension = file.filename.split(".")[-1]

    file_path = UPLOAD_DIR / f"{file_id}.{extension}"

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    return {
        "status": "ok",
        "file_id": file_id,
        "file_type": "handwritten",
        "file_path": str(file_path)
    }

