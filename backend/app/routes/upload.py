from fastapi import APIRouter

router = APIRouter()

@router.post("/upload/text")
def upload_text():
    return {"status": "ok"}
