from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes.upload import router as upload_router

app = FastAPI(title="Custom Handwriting Converter")  # 👈 THIS MUST BE NAMED app

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Backend is running"}
