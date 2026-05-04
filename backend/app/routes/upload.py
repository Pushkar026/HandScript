from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
from pathlib import Path
import uuid
import os

import cloudinary
import cloudinary.uploader

from dotenv import load_dotenv

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()

ENV = os.getenv("ENV", "development")  # default = development

# -----------------------------
# Configure Cloudinary
# -----------------------------
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

router = APIRouter()

# -----------------------------
# Base directory
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# -----------------------------
# Upload directory
# -----------------------------
UPLOAD_DIR = BASE_DIR / "uploads" / "input"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


class TextUpload(BaseModel):
    text: str


# ------------------------------------------------
# Upload text file
# ------------------------------------------------
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


# ------------------------------------------------
# Upload handwritten template
# ------------------------------------------------
@router.post("/upload/handwritten")
def upload_handwritten(file: UploadFile = File(...)):

    file_id = str(uuid.uuid4())
    extension = file.filename.split(".")[-1]

    temp_file_path = UPLOAD_DIR / f"{file_id}.{extension}"

    # Save file locally first
    with open(temp_file_path, "wb") as f:
        f.write(file.file.read())

    # -----------------------------
    # ENV-based logic
    # -----------------------------
    if ENV == "development":
        # 👉 Local storage
        return {
            "status": "ok",
            "file_id": file_id,
            "file_type": "handwritten",
            "local_path": str(temp_file_path)
        }

    else:
        # 👉 Cloudinary upload
        upload_result = cloudinary.uploader.upload(
            str(temp_file_path),
            folder="handscript_templates",
            public_id=file_id
        )

        # Delete temp file after upload
        os.remove(temp_file_path)

        return {
            "status": "ok",
            "file_id": file_id,
            "file_type": "handwritten",
            "cloudinary_url": upload_result["secure_url"]
        }