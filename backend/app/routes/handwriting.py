from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import uuid

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "uploads" / "custom_handwriting"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/upload/handwriting")
async def upload_handwriting(file: UploadFile = File(...)):
    if file.content_type not in [
        "image/png",
        "image/jpeg",
        "application/pdf"
    ]:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    file_id = f"{uuid.uuid4().hex}_{file.filename}"
    file_path = UPLOAD_DIR / file_id

    with open(file_path, "wb") as f:
        f.write(await file.read())

    return {
        "message": "Handwriting template uploaded successfully",
        "file_id": file_id
    }
