from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from .routes.upload import router as upload_router
from .routes.convert import router as convert_router
from .routes.handwriting import router as handwriting_router

BASE_DIR = Path(__file__).resolve().parent

STATIC_DIR = BASE_DIR / "static"
STATIC_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="HandScript API")

# -----------------------------------
# CORS
# -----------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------------
# Routes
# -----------------------------------
app.include_router(upload_router, prefix="/api")

app.include_router(convert_router, prefix="/api")

app.include_router(handwriting_router, prefix="/api")

# -----------------------------------
# Static template files
# -----------------------------------
app.mount(
    "/static",
    StaticFiles(directory=STATIC_DIR),
    name="static"
)

# -----------------------------------
# Health check route
# -----------------------------------
@app.get("/")
def root():
    return {
        "message": "HandScript backend is running"
    }