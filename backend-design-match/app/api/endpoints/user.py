from fastapi import APIRouter

router = APIRouter()


@router.get("/me")
async def get_user_profile():
    return {"message": "User profile endpoint"}


@router.put("/me")
async def update_user_profile():
    return {"message": "Update profile endpoint"}
