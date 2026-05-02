from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import uuid
import os

import cloudinary
import cloudinary.uploader

from dotenv import load_dotenv

# ---------------------------------
# Load environment variables
# ---------------------------------
load_dotenv()

# ---------------------------------
# Configure Cloudinary
# ---------------------------------
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

router = APIRouter()

# ---------------------------------
# Temp upload directory
# ---------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

UPLOAD_DIR = BASE_DIR / "uploads" / "custom_handwriting"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/upload/handwriting")
async def upload_handwriting(file: UploadFile = File(...)):

    # ---------------------------------
    # Validate file type
    # ---------------------------------
    if file.content_type not in [
        "image/png",
        "image/jpeg",
        "application/pdf"
    ]:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type"
        )

    # ---------------------------------
    # Generate unique file name
    # ---------------------------------
    unique_id = uuid.uuid4().hex

    extension = file.filename.split(".")[-1]

    temp_file_name = f"{unique_id}.{extension}"

    temp_file_path = UPLOAD_DIR / temp_file_name

    # ---------------------------------
    # Save temporarily
    # ---------------------------------
    with open(temp_file_path, "wb") as f:
        f.write(await file.read())

    # ---------------------------------
    # Upload to Cloudinary
    # ---------------------------------
    upload_result = cloudinary.uploader.upload(
        str(temp_file_path),
        folder="handscript/custom_handwriting",
        public_id=unique_id
    )

    # ---------------------------------
    # Delete local temp file
    # ---------------------------------
    os.remove(temp_file_path)

    return {
        "message": "Handwriting template uploaded successfully",
        "file_id": unique_id,
        "cloudinary_url": upload_result["secure_url"]
    }