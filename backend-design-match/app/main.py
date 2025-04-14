import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from tortoise.contrib.fastapi import register_tortoise

from validation.upload import router as upload_router
from validation.validate import router as validate_router
from auth.routes import auth_router

app = FastAPI(title="DesignMatch API", version="1.0")

# Enable CORS for frontend interaction
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this to restrict access in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(upload_router, prefix="/upload", tags=["Upload"])
app.include_router(validate_router, prefix="/validate", tags=["Validate"])


# SQLite Database Configuration
register_tortoise(
    app,
    db_url="sqlite://users.db",
    modules={"models": ["auth.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)


# Redirect root ("/") to Swagger UI docs ("/docs")
@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")


# Run the app using: uvicorn app.main:app --reload

os.environ["PATH"] += os.pathsep + r"C:\Path\To\GTK\bin"
import pytesseract

# Set the Tesseract command path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
