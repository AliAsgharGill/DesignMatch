from datetime import timedelta

from auth.models import User, UserCreate
from auth.utils import (create_access_token, create_refresh_token,
                        decode_token, hash_password, verify_password)
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from .models import UserLogin

auth_router = APIRouter()


@auth_router.post("/register")
async def register(user_data: UserCreate):
    """
    Register a new user.

    Args:
        user_data (UserCreate): User registration data containing:
            - email (str): User's email address.
            - username (str): User's chosen username.
            - password (str): User's password (plaintext).
            - role (UserRole, optional): User's role (default: "user").

    Returns:
        dict:
            - message (str): Success message.
            - user_id (int): The unique ID of the newly created user.
    """
    existing_user = await User.filter(email=user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user_data.password)
    user = await User.create(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hashed_password,
        role=user_data.role,
    )

    return {"message": "User registered successfully", "user_id": user.id}


from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm


@auth_router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Authenticate a user and return access and refresh tokens.

    Args:
        form_data (OAuth2PasswordRequestForm): Form data containing:
            - username (str): User's email (used as username).
            - password (str): User's password.

    Returns:
        dict:
            - access_token (str): JWT access token.
            - refresh_token (str): JWT refresh token.
            - token_type (str): "bearer".
    """
    try:
        user = await User.get(
            email=form_data.username
        )  # OAuth2PasswordRequestForm uses 'username' instead of 'email'
    except DoesNotExist:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid password")

    access_token = create_access_token(data={"sub": user.email, "role": user.role})
    refresh_token = create_refresh_token(data={"sub": user.email})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@auth_router.post("/refresh")
async def refresh_token(refresh_token: str):
    """
    Generate a new access token using a refresh token.

    Args:
        refresh_token (str): The refresh token provided during login.

    Returns:
        dict:
            - access_token (str): New JWT access token.
            - token_type (str): Token type (always "bearer").

    Raises:
        HTTPException (401): If the refresh token is invalid or expired.
    """
    try:
        decoded_data = decode_token(refresh_token, is_refresh=True)
        email = decoded_data.get("sub")

        user = await User.get(email=email)
        access_token = create_access_token(data={"sub": user.email, "role": user.role})

        return {"access_token": access_token, "token_type": "bearer"}
    except:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
