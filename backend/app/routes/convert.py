from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pathlib import Path
import uuid
import os

import cloudinary
import cloudinary.uploader

from dotenv import load_dotenv

from app.services.extractor import extract_text
from app.services.renderer import render_handwritten_text
from app.services.fonts import FONT_MAP

# -----------------------------------
# Load environment variables
# -----------------------------------
load_dotenv()

ENV = os.getenv("ENV", "development")

# -----------------------------------
# Configure Cloudinary
# -----------------------------------
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

router = APIRouter()

# -----------------------------------
# Base directories
# -----------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

UPLOAD_DIR = BASE_DIR / "uploads" / "input"

OUTPUT_DIR = BASE_DIR / "uploads" / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

BACKGROUND_PATH = (
    BASE_DIR / "assets" / "backgrounds" / "notebook.jpg"
)

# -----------------------------------
# Request model
# -----------------------------------
class ConvertRequest(BaseModel):
    file_id: str
    file_type: str
    font_key: str | None = "handwriting"


# -----------------------------------
# Convert endpoint
# -----------------------------------
@router.post("/convert")
def convert_file(data: ConvertRequest):

    # -----------------------------------
    # Only text supported for now
    # -----------------------------------
    if data.file_type != "text":
        raise HTTPException(
            status_code=400,
            detail="Only text conversion supported for now"
        )

    # -----------------------------------
    # Find uploaded text file
    # -----------------------------------
    input_file = UPLOAD_DIR / f"{data.file_id}.txt"

    if not input_file.exists():
        raise HTTPException(
            status_code=404,
            detail="Input file not found"
        )

    # -----------------------------------
    # Extract text
    # -----------------------------------
    extracted_text = extract_text(
        input_file,
        data.file_type
    )

    if not extracted_text.strip():
        raise HTTPException(
            status_code=400,
            detail="Extracted text is empty"
        )

    # -----------------------------------
    # Resolve font
    # -----------------------------------
    font_path = FONT_MAP.get(data.font_key)

    if not font_path:
        raise HTTPException(
            status_code=400,
            detail="Invalid font selected"
        )

    # -----------------------------------
    # Generate output image
    # -----------------------------------
    output_id = str(uuid.uuid4())
    output_path = OUTPUT_DIR / f"{output_id}.png"

    render_handwritten_text(
        text=extracted_text,
        output_path=output_path,
        font_path=Path(font_path),
        background_path=BACKGROUND_PATH,
    )

    # -----------------------------------
    # ENV-based logic
    # -----------------------------------
    if ENV == "development":
        # 👉 keep locally
        image_url = f"/uploads/output/{output_id}.png"

    else:
        # 👉 upload to Cloudinary
        upload_result = cloudinary.uploader.upload(
            str(output_path),
            folder="handscript/generated_outputs",
            public_id=output_id
        )

        image_url = upload_result["secure_url"]

        # delete local file after upload
        os.remove(output_path)

    return {
        "status": "ok",
        "output_id": output_id,
        "image_url": image_url   # ✅ unified response
    }