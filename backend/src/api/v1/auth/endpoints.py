from fastapi import APIRouter, Depends

from . import schemas
from src.api.v1.auth.dependencies import get_auth_by_telegram
from src.application.auth.commands import AuthByTelegramCommand
from src.application.auth.use_cases.by_telegram import AuthByTelegram

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/telegram", response_model=schemas.AuthResponse)
async def auth_telegram_endpoint(
	payload: schemas.TelegramAuthRequest,
	auth_by_telegram: AuthByTelegram = Depends(get_auth_by_telegram)
):
	command = AuthByTelegramCommand(**payload.model_dump())
	result = await auth_by_telegram.execute(command=command)
	return schemas.AuthResponse(access_token=result.access_token, refresh_token=result.refresh_token)
