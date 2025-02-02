# app/main.py
from api.endpoints.auth import router as auth_router
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


@app.get("/")
async def root():
    return {"message": "Welcome to Design Match API"}


# Run the app using: uvicorn app.main:app --reload
