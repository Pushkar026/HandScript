from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes.upload import router as upload_router
from .routes.convert import router as convert_router

app = FastAPI(title="Custom Handwriting Converter")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(upload_router, prefix="/api")
app.include_router(convert_router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Backend is running"}

