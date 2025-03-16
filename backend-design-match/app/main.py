import os
from fastapi import FastAPI
from auth.routes import auth_router
from api.   endpoints.upload import router as upload_router
from api.endpoints.validate import router as validate_router
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise



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


# SQLite Database Configuration
register_tortoise(
    app,
    db_url="sqlite://users.db",
    modules={"models": ["auth.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)


@app.get("/")
async def root():
    return {"message": "Welcome to Design Match API"}


# Run the app using: uvicorn app.main:app --reload

os.environ["PATH"] += os.pathsep + r"C:\Path\To\GTK\bin"
