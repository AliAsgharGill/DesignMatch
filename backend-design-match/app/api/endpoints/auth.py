from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/login")
async def login():
    return {"message": "Login endpoint"}


@router.post("/register")
async def register():
    return {"message": "Register endpoint"}
