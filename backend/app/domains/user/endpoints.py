from fastapi import APIRouter, Depends

from app.domains.auth.dependencies import get_current_user
from .schemas import User

router = APIRouter(prefix="/api/v1/users", tags=["Users"])

@router.get("/me", response_model=User)
async def me_endpoint(user: User = Depends(get_current_user)):
	return user
