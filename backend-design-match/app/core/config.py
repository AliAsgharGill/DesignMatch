from config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from fastapi import APIRouter, Depends

router = APIRouter()


@router.post("/login")
async def login():
    # print("SECRET_KEY:", SECRET_KEY)  # Just for testing (remove in production)
    return {"message": "Login successful"}
