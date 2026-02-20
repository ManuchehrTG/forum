from pydantic import BaseModel, Field

class TelegramAuthRequest(BaseModel):
	init_data: str = Field(..., description="InitData from Telegram WebApp")

class AuthResponse(BaseModel):
	access_token: str = Field(..., description="access_token")
	refresh_token: str | None = Field(..., description="refresh_token")
