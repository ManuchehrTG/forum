from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, field_validator
from uuid import UUID

class ThemeTechVersionType(str, Enum):
	FULL = "full"
	MINIMUM = "minimum"

class ThemeCreateRequest(BaseModel):
	title: str = Field(..., min_length=3, max_length=32, description="Название темы")
	parent_id: int | None = Field(None, description="ID родительской темы", examples=[None])
	tech_version: ThemeTechVersionType = Field(default="full", description="Принадлежность к техно-деревне")

	@field_validator("title")
	@classmethod
	def validate_title(cls, v: str) -> str:
		stripped = v.strip()
		if len(stripped) < 3:  # Проверяем длину без пробелов
			raise ValueError("Title must have at least 3 non-whitespace characters")
		return stripped

class Theme(BaseModel):
	id: int = Field(..., description="Уникальный ID темы")
	parent_id: int | None = Field(None, description="ID родительской темы")
	author_id: UUID | None = Field(None, description="ID автора темы")
	title: str = Field(..., max_length=32, description="Название темы")
	is_group: bool = Field(False, description="Является ли группой")
	created_at: datetime = Field(..., description="Дата создания темы")
	updated_at: datetime = Field(..., description="Дата изменения темы")

class ThemeResponse(Theme):
	pass
