from fastapi import APIRouter, Depends

from . import schemas
from src.api.v1.users.dependencies import get_current_user
from src.application.users.dtos import UserDTO

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=schemas.UserResponse, summary="Get me", description="<b>Получить свои данные.</b>")
async def get_current_user_info_endpoint(
	current_user: UserDTO = Depends(get_current_user)
):
	return schemas.UserResponse.model_validate(current_user.model_dump())
