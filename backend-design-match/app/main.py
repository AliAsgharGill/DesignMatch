import os

from api.endpoints.auth import router as auth_router
from api.endpoints.generate_report import router as generate_report_router
from api.endpoints.upload import router as upload_router
from api.endpoints.validate import router as validate_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Design Match API", version="1.0")

# Enable CORS for frontend interaction


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this to restrict access in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(upload_router, prefix="/upload", tags=["upload"])
app.include_router(validate_router, prefix="/validate", tags=["validate"])
app.include_router(generate_report_router, prefix="/api/v1", tags=["reports"])


@app.get("/")
async def root():
    return {"message": "Welcome to Design Match API"}


# Run the app using: uvicorn app.main:app --reload

os.environ["PATH"] += os.pathsep + r"C:\Path\To\GTK\bin"
