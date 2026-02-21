import uuid
from datetime import date, datetime
from pydantic import BaseModel, Field

class UserResponse(BaseModel):
	id: uuid.UUID = Field(..., description="ID пользователя")

	first_name: str = Field(..., description="Имя пользователя")
	last_name: str | None = Field(None, description="Фамилия пользователя")
	username: str | None = Field(None, description="Уникальный Username пользователя")
	about: str | None = Field(None, description="О пользователе (в шапке профиля)")
	location: str | None = Field(None, description="Локация пользователя (в шапке профиля)")
	birthday: date | None = Field(None, description="День рождение пользователя")
	language_code: str = Field(..., description="Язык пользователя")
	avatar_path: str | None = Field(None, description="Путь к аватарке пользователя на сервере")

	# email: str | None = Field(None, description="Email пользователя")
	# phone: str | None = Field(None, description="Телефон пользователя")

	# created_at: datetime
	# updated_at: datetime
