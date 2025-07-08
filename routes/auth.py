from fastapi import APIRouter, Depends, HTTPException, status
from models.user import User
from auth.dependencies import get_current_user, require_role

router = APIRouter()

@router.get("/me")
async def read_current_user(current_user: User = Depends(get_current_user)):
    require_role("seller")(current_user)
    return {
        "id": current_user.id,
        "email": current_user.email,
        "role": current_user.role
    }