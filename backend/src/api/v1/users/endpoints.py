from fastapi import APIRouter, Depends

from . import schemas
from src.api.v1.users.dependencies import get_current_user
from src.application.users.dtos import UserDTO

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=schemas.UserResponse)
async def get_current_user_info_endpoint(
	current_user: UserDTO = Depends(get_current_user)
):
	return schemas.UserResponse.from_orm(current_user)
