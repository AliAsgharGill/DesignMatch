from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from auth.models import UserRole
from auth.utils import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    if not token:
        raise HTTPException(status_code=401, detail="Token is missing")  # Ensure token is required

    try:
        payload = decode_token(token)
        email = payload.get("sub")
        role = payload.get("role")
        if email is None or role is None:
            raise HTTPException(status_code=401, detail="Invalid token data")
        return {"email": email, "role": role}
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

async def admin_required(user: dict = Depends(get_current_user)):
    if user["role"] != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Admin access required")
    return user
