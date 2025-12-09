from datetime import datetime
from pydantic import BaseModel, Field
from uuid import UUID

class UserCreateData(BaseModel):
	first_name: str
	username: str | None = None
	email: str | None = None
	phone_number: str | None = None
	language_code: str
	avatar_url: str | None = None

class User(UserCreateData):
	id: UUID
	created_at: datetime
	updated_at: datetime



# class UserPublicResponse(BaseModel):
# 	id: UUID = Field(..., description="Уникальный ID пользователя")
# 	username: str | None = Field(None, description="Юзернейм пользователя")
# 	first_name: str = Field(..., description="Имя пользователя")
# 	avatar_url: str | None = Field(None, description="Ссылка на аватар пользователя")
# 	language_code: str = Field(settings.DEFAULT_LANGUAGE, description="Язык пользователя")

# class UserPrivateResponse(UserPublicResponse):
# 	# telegram_id: int | None = Field(None, description="Уникальный ID пользователя Telegram")
# 	email: str | None = Field(None, description="Email пользователя")
# 	phone_number: str | None = Field(None, description="Номер телефона пользователя")
# 	created_at: datetime = Field(..., description="Дата создания")
# 	updated_at: datetime = Field(..., description="Дата обновления")


# class UserPublicResponse(BaseModel):
# 	id: int = Field(..., description="Уникальный ID пользователя")
# 	username: str | None = Field(None, description="Юзернейм пользователя")
# 	first_name: str = Field(..., description="Имя пользователя")
# 	avatar_url: str | None = Field(None, description="Ссылка на аватар пользователя")
# 	language_code: str = Field(settings.DEFAULT_LANGUAGE, description="Язык пользователя")

# class UserCreateTelegramData(UserPublicResponse):
# 	photo_url: str = Field(..., description="Ссылка на фото профиля в Телеграмме")


# class UserPrivateResponse(UserPublicResponse):
# 	telegram_id: int | None = Field(None, description="Уникальный ID пользователя Telegram")
# 	email: str | None = Field(None, description="Email пользователя")
# 	phone_number: str | None = Field(None, description="Номер телефона пользователя")
# 	created_at: datetime = Field(..., description="Дата создания")
# 	updated_at: datetime = Field(..., description="Дата обновления")
