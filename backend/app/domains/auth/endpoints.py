from fastapi import APIRouter, Depends, HTTPException

from app.domains.user.schemas import User
from .dependencies import get_auth_service, get_current_user
from .schemas import TelegramLoginRequest, AuthResponse
from .services import AuthService

router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])

@router.post("/telegram/login", response_model=AuthResponse)
async def telegram_login_endpoint(
	payload: TelegramLoginRequest,
	auth_service: AuthService = Depends(get_auth_service)
):
	token = await auth_service.telegram_login(payload=payload)
	return AuthResponse(token=token)

# @router.post("/telegram/link", response_model=AuthResponse)
# async def telegram_link_endpoint(
# 	payload: TelegramLoginRequest,
# 	auth_service: AuthService = Depends(get_auth_service),
# 	user: User = Depends(get_user)
# ):
# 	token = await auth_service.telegram_link(user=user, payload=payload)
# 	return AuthResponse(token=token)
