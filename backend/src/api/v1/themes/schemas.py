from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field
from uuid import UUID

class TechVersionTypeAPI(str, Enum):
	FULL = "full"
	MINIMUM = "minimum"

class ThemeCreateRequest(BaseModel):
	parent_id: UUID | None = Field(None, description="ID родителя")
	title: str = Field(..., min_length=3, max_length=32, description="Название")
	is_group: bool = Field(False, description="Является группой")
	tech_version: TechVersionTypeAPI = Field(default=TechVersionTypeAPI.FULL, description="Принадлежность к техно-деревне")

class ThemeResponse(BaseModel):
	id: UUID = Field(..., description="ID темы")

	parent_id: UUID | None = Field(None, description="ID родителя")
	author_id: UUID | None = Field(None, description="ID автора")
	title: str = Field(..., description="Название")
	is_group: bool = Field(..., description="Является группой")

	created_at: datetime = Field(..., description="Дата и время создания")
	updated_at: datetime = Field(..., description="Дата и вермя обновления")

	class Config:
		from_attributes = True

class ThemeSectionResponse(BaseModel):
	section_id: UUID = Field(..., description="ID секции")
	section_code: str = Field(..., description="Code секции")

	class Config:
		from_attributes = True
