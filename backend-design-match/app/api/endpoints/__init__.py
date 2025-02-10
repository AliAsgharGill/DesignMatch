from fastapi import APIRouter
from .deep_validate import router as deep_validate_router  # Import the new route


api_router = APIRouter()

# Include existing and new routes
api_router.include_router(deep_validate_router, prefix="/validate", tags=["Deep Validation"])
