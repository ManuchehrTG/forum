from enum import Enum
from pydantic import BaseModel, Field, field_validator

from app.core.config import settings

class AuthProviderType(str, Enum):
	PASSWORD = "password"
	TELEGRAM = "telegram"

class TelegramLoginRequest(BaseModel):
	init_data: str = Field(..., description="InitData from Telegram WebApp")

class TelegramData(BaseModel):
	id: str = Field(..., description="Уникальный ID Telegram пользователя")
	username: str | None = Field(None, description="Юзернейм пользователя")
	first_name: str = Field(..., description="Имя пользователя")
	language_code: str | None = Field(None, description="Язык пользователя")
	photo_url: str | None = Field(None, description="Ссылка на аватар пользователя")

	@field_validator("id", mode="before")
	@classmethod
	def convert_id(cls, value: int) -> str:
		return str(value)

	@field_validator("language_code", mode="before")
	@classmethod
	def validate_language_code(cls, value: str | None) -> str:
		if value not in settings.LANGUAGES:
			return settings.DEFAULT_LANGUAGE
		return value

class AuthResponse(BaseModel):
	token: str = Field(..., description="JWT токен")
	message: str = Field(default="Authenticated successfully", description="Ответ")
	status: str = Field(default="ok", description="Status")

